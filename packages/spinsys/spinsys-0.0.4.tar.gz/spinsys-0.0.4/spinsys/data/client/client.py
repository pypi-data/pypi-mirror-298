# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import os
import functools
import typing

from fsspec import spec  # type: ignore


import spinsys.spin as spin
import spinsys.data as data
from .file import File
from .options import Options


class Client:
    def __init__(self, options: Options):
        self.options = options

    def namespace(self, ctzn: spin.Name):
        return Namespace(self, ctzn)

    def put(
        self, address: data.BlockAddress, bs: bytes
    ) -> tuple[typing.Optional[data.StoreRef], typing.Optional[spin.Error]]:
        return None, spin.ErrNotImplemented

    @functools.lru_cache(maxsize=2000)
    def get(
        self, addr: data.BlockAddress, ref: data.BlockReference
    ) -> tuple[typing.Optional[bytes], typing.Optional[spin.Error]]:
        if self.options.store is None:
            return None, spin.ErrNotImplemented

        bs, _, err = self.options.store.get(addr, ref)
        if err:
            return None, err

        return bs, None

    def delete(self, address: data.BlockAddress) -> typing.Optional[spin.Error]:
        return spin.ErrNotImplemented

    def _lookup(
        self, ctzn: spin.Name, path: spin.Path
    ) -> tuple[typing.Optional[data.Entry], typing.Optional[spin.Error]]:
        if self.options.dir_server is None:
            return None, spin.ErrNotImplemented

        resp = self.options.dir_server.list(
            data.DirListRequest(
                public=self.options.public,
                private=self.options.private,
                citizen=ctzn,
                path=path,
                level=0,
            )
        )
        if resp.error != "":
            return None, spin.error_from_string(resp.error)
        if len(resp.entries) != 1:
            raise OSError(f"expected 1 entry, got {len(resp.entries)}")
        return resp.entries[0], None

    def _read_directory(
        self, ctzn: spin.Name, path: spin.Path
    ) -> tuple[typing.Optional[list[data.Entry]], typing.Optional[spin.Error]]:
        if self.options.dir_server is None:
            return None, spin.ErrNotImplemented

        resp = self.options.dir_server.list(
            data.DirListRequest(
                public=self.options.public,
                private=self.options.private,
                citizen=ctzn,
                path=path,
                level=1,
            )
        )
        if resp.error != "":
            return None, spin.error_from_string(resp.error)

        return resp.entries[1:], None  # exclude the root

    def _ensureDirectory(
        self, ctzn: spin.Name, path: spin.Path, no_prior: bool = False
    ) -> tuple[typing.Optional[data.Entry], typing.Optional[spin.Error]]:
        if self.options.dir_server is None:
            return None, spin.ErrNotImplemented

        resp = self.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.options.public,
                private=self.options.private,
                ops=[
                    data.DirOp(
                        type=data.DirOpType.PutDirOp,
                        entry=data.Entry(
                            citizen=ctzn,
                            path=path,
                            type=data.EntryType.DirectoryEntry,
                            time=self.options.get_time(),
                            version=data.NoPriorVersion
                            if no_prior
                            else data.IgnoreVersion,
                        ),
                    )
                ],
            )
        )

        if resp.error != "":
            return None, spin.error_from_string(resp.error)

        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return resp.outcomes[0].entry, None

    def _ensureDirectoryAllPath(
        self,
        ctzn: spin.Name,
        p: spin.Path,
        frm: spin.Path,
        no_prior: bool = False,
    ) -> tuple[typing.Optional[list[data.Entry]], typing.Optional[spin.Error]]:
        if frm != "" and not spin.path_is_ancestor(frm, p):
            return None, spin.Error(f"{frm} is not an ancestor of {p}")

        if self.options.dir_server is None:
            return None, spin.ErrNotImplemented

        ps = spin.path_sequence(p)
        ops = []
        for p in ps:
            if frm != "" and spin.path_is_ancestor(p, frm):
                continue  # skip the path if it is an ancestor of frm

            ops.append(
                data.DirOp(
                    type=data.DirOpType.PutDirOp,
                    entry=data.Entry(
                        citizen=ctzn,
                        path=p,
                        type=data.EntryType.DirectoryEntry,
                        time=self.options.get_time(),
                        version=data.NoPriorVersion if no_prior else data.IgnoreVersion,
                    ),
                )
            )

        resp = self.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.options.public,
                private=self.options.private,
                ops=ops,
            )
        )

        if resp.error != "":
            return None, spin.error_from_string(resp.error)

        if len(resp.entries) != len(ops):
            raise OSError(f"expected {len(ops)} entries, got {len(resp.entries)}")

        return resp.entries, None

    def _open(
        self,
        ctzn: spin.Name,
        path: spin.Path,
        mode="rb",
        block_size="default",
        **kwargs,
    ) -> File:
        return File(
            self.namespace(ctzn).fs(),
            path,
            mode=mode,
            block_size=block_size,
            **kwargs,
        )


class Namespace:
    def __init__(self, client: Client, ctzn: spin.Name):
        if "/" in ctzn:
            raise ValueError(f"invalid name: {ctzn}")

        self.client = client
        self.ctzn = ctzn
        self.root = spin.Path("/")

    def _fullPath(self, name: str) -> str:
        return os.path.join(self.root, name)

    def change_directory(self, name: str):
        self.root = os.path.join(self.root, name)

    def lookup(
        self, name: str
    ) -> tuple[typing.Optional[data.Entry], typing.Optional[spin.Error]]:
        return self.client._lookup(self.ctzn, self._fullPath(name))

    def read_directory(
        self, name: str
    ) -> tuple[typing.Optional[list[data.Entry]], typing.Optional[spin.Error]]:
        return self.client._read_directory(self.ctzn, self._fullPath(name))

    def make_directory(
        self, name: str, no_prior=False
    ) -> tuple[typing.Optional[data.Entry], typing.Optional[spin.Error]]:
        return self.client._ensureDirectory(
            self.ctzn, self._fullPath(name), no_prior=no_prior
        )

    def make_directory_all(
        self, name: str, no_prior=False
    ) -> tuple[typing.Optional[list[data.Entry]], typing.Optional[spin.Error]]:
        return self.client._ensureDirectoryAllPath(
            self.ctzn, self._fullPath(name), self.root, no_prior=no_prior
        )

    def open(
        self, name: str, mode="rb", block_size="default", **kwargs
    ) -> typing.Union[File, spin.Error]:
        return self.client._open(self.ctzn, self._fullPath(name))

    def fs(self) -> "FileSystem":
        return FileSystem(self)


class FileSystem(spec.AbstractFileSystem):
    """
    Helper class for a fsspec file system.

    Note: This is based off of the Databricks filesystem implementation which
    can be found here:
    https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py
    """

    protocol = "spin"
    root_marker = "/"

    def __init__(self, ns: Namespace, *args, **kwargs):
        self.ns = ns

        super().__init__(*args, **kwargs)

    def ls(self, path: str, detail: bool = True, refresh=False):
        """
        List the contents of the given path.

        Parameters
        ----------
        path: str
            Absolute path
        detail: bool
            Return not only the list of filenames,
            but also additional information on file sizes
            and types.
        """

        if refresh:
            self.invalidate_cache(path)

        out = self._ls_from_cache(path)
        if not out:
            entries, err = self.ns.read_directory(path)
            if err:
                if err == spin.ErrNotFound:
                    raise FileNotFoundError(path)
                else:
                    raise Exception(f"path {path} error: {err}")
            if entries is None:
                entries = []

            out = [
                {
                    # the first three here are required
                    "name": e.path,
                    "type": "directory"
                    if e.type == data.EntryType.DirectoryEntry
                    else "file",
                    "size": sum([b.size for b in e.blocks]),
                    "ctime": e.created_at * 1_000_000,
                    "mtime": e.updated_at * 1_000_000,
                }
                for e in entries
            ]
            self.dircache[path.rstrip("/")] = out

        if detail:
            return out
        else:
            return sorted([o["name"] for o in out])

    def makedirs(self, path, exist_ok=True):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        exist_ok: bool
            If false, checks if the folder
            exists before creating it (and raises an
            Exception if this is the case)
        """
        out, err = self.ns.make_directory_all(path)
        if err:
            raise Exception(err)

        for e in out:
            self.invalidate_cache(self._parent(e.path))

    def mkdir(self, path, create_parents=True, **kwargs):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        create_parents: bool
            Whether to create all parents or not.
            "False" is not implemented so far.
        """
        if not create_parents:
            return self.ns.make_directory(path, **kwargs)

        out = self.mkdirs(path, **kwargs)
        if isinstance(out, spin.Error):
            raise Exception(out)

        self.invalidate_cache(self._parent(path))

    def cp_file(self, frompath, topath, **kwargs):
        e, err = self._lookup(frompath)
        if err:
            if err == spin.ErrNotFound:
                raise FileNotFoundError(f"path {frompath}")
            else:
                raise Exception(f"path {frompath} error: {err}")

        ne = data.Entry(
            citizen=e.citizen,
            path=topath,
            version=data.IgnoreVersion,
            time=self.ns.client.options.get_time(),
            type=e.type,
            pack_type=e.pack_type,
            pack_data=e.pack_data,
            blocks=e.blocks,
            license=e.license,
        )
        resp = self.ns.client.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.ns.client.options.public,
                private=self.ns.client.options.private,
                ops=[
                    data.DirOp(
                        type=data.DirOpType.PutDirOp,
                        entry=ne,
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(resp.error)
        self.invalidate_cache(self._parent(topath))

    def rm_file(self, path):
        resp = self.ns.client.options.dir_server.apply(
            data.DirApplyRequest(
                public=self.ns.client.options.public,
                private=self.ns.client.options.private,
                ops=[
                    data.DirOp(
                        type=data.DirOpType.DelDirOp,
                        entry=data.Entry(
                            citizen=self.ns.ctzn,
                            path=path,
                            version=data.IgnoreVersion,
                        ),
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(f"dir server apply: {resp.error}")
        self.invalidate_cache(self._parent(path))

    def _open(self, path, mode="rb", block_size="default", **kwargs):
        """
        Overwrite the base class method to make sure to create a File.
        All arguments are copied from the base method.
        """
        return File(self, path, mode=mode, block_size=block_size, **kwargs)

    # lookup a dir entry
    def _lookup(
        self, path: spin.Path
    ) -> tuple[typing.Optional[data.Entry], typing.Optional[spin.Error]]:
        return self.ns.client._lookup(self.ns.ctzn, path)

    def _get(
        self, addr: data.BlockAddress, ref: data.BlockReference
    ) -> tuple[typing.Optional[bytes], typing.Optional[spin.Error]]:
        return self.ns.client.get(addr, ref)

    def invalidate_cache(self, path=None):
        if path is None:
            self.dircache.clear()
        else:
            self.dircache.pop(path, None)
        super().invalidate_cache(path)

    def chmod(self, path, mode):
        print(f"not implemented chmod: {path} {mode}")
        raise NotImplementedError
        pass
