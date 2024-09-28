# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

from concurrent.futures import ThreadPoolExecutor, as_completed

from fsspec import spec  # type: ignore

import spinsys.spin as spin
import spinsys.data as data


class File(spec.AbstractBufferedFile):
    """
    Helper class for files referenced by the FileSystem.

    Note: This is based off of the Databricks filesystem implementation which
    can be found here:
    https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py.
    """

    def __init__(
        self,
        fs,
        path,
        mode="rb",
        block_size="default",
        autocommit=True,
        cache_type="readahead",
        cache_options=None,
        **kwargs,
    ):
        if block_size is None or block_size == "default":
            block_size = fs.ns.client.options.block_size

        self.dir_entry = None

        super().__init__(
            fs,
            path,
            mode=mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_type=cache_type,
            cache_options=cache_options or {},
            **kwargs,
        )

    def _initiate_upload(self):
        """
        Internal function to start a file upload.
        Only plain pack is supported at present.
        """
        pt = self.fs.ns.client.options.pack_type
        if pt != data.PackType.MissingPackType and pt != data.PackType.PlainPack:
            raise NotImplementedError(f"Pack type {pt} not implemented")
        if pt == data.PackType.MissingPackType:
            pt = data.PackType.PlainPack

        self.dir_entry = data.Entry(
            type=data.EntryType.FileEntry,
            citizen=self.fs.ns.ctzn,
            path=self.path,
            version=data.IgnoreVersion,
            pack_type=pt,
        )

    def _upload_chunk(self, final=False):
        """
        Internal function to add a chunk of data to a started upload.
        """

        self.buffer.seek(0)
        bs = self.buffer.getvalue()

        data_chunks = [bs[start:end] for start, end in self._to_sized_blocks(len(bs))]

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            sizes = []
            for data_chunk in data_chunks:
                futures.append(
                    executor.submit(
                        self.fs.ns.client.options.store.put,
                        data.AnyAddress,
                        data_chunk,
                    )
                )
                sizes.append(len(data_chunk))

            for i, (size, future) in enumerate(zip(sizes, as_completed(futures))):
                store_ref, err = future.result()
                if err:
                    raise OSError(f"store put: {err}")
                self.dir_entry.blocks.append(
                    data.EntryBlock(
                        address=store_ref.address,
                        reference=store_ref.reference,
                        offset=self.offset + i * self.blocksize,
                        size=len(data_chunk),
                    )
                )

        if final:
            resp = self.fs.ns.client.options.dir_server.apply(
                data.DirApplyRequest(
                    public=self.fs.ns.client.options.public,
                    private=self.fs.ns.client.options.private,
                    ops=[
                        data.DirOp(type=data.DirOpType.PutDirOp, entry=self.dir_entry)
                    ],
                )
            )
            if resp.error != "":
                raise OSError(f"dir ops upload: {resp.error}")

            self.dir_entry = resp.entries[0]
            self.fs.invalidate_cache(self.fs._parent(self.dir_entry.path))
            return True

    # warn: this code is not seriously tested
    def _intersection(self, a, b, c, d):
        # compute [a, b] ∩ [c,d]
        if b < c or a > d:
            return (0, 0)
        return (max(a, c), min(b, d))

    # warn: this code is not seriously tested
    def _blocks_in_range(self, start, end):
        # find the blocks for the file for the bit range start to end
        out = []
        for b in self.dir_entry.blocks:
            bstart, bend = b.offset, b.offset + b.size
            istart, iend = self._intersection(start, end, bstart, bend)
            if iend - istart == 0:  # skip if empty intersection
                continue
            out.append((b, (istart, iend)))
        return out

    def _fetch_range(self, start, end):
        """
        Internal function to download a block of data
        """
        if self.dir_entry is None:
            e, err = self.fs._lookup(self.path)
            if err:
                if err == spin.ErrNotFound:
                    raise FileNotFoundError
                else:
                    raise Exception(f"path {self.path} error: {err}")
            self.dir_entry = e

        if self.dir_entry.pack_type != data.PackType.PlainPack:
            raise NotImplementedError(
                f"Pack type {self.dir_entry.pack_type} not implemented"
            )

        return_buffer = b""
        for b, (s, e) in self._blocks_in_range(start, end):
            dat, err = self.fs._get(b.address, b.reference)
            if err:
                raise Exception(f"block {b} error: {err}")
            return_buffer += dat[start - b.offset : end]
        return return_buffer

    def _to_sized_blocks(self, total_length):
        """
        Helper function to split a range from 0 to total_length into blocksizes
        """
        for data_chunk in range(0, total_length, self.blocksize):
            data_start = data_chunk
            data_end = min(total_length, data_chunk + self.blocksize)
            yield data_start, data_end
