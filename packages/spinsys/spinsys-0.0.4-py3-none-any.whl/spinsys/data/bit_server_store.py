# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import typing

import spinsys.spin as spin
from .bit_server import BitOpsRequest
from .bit_ops import BitOp, BitOpType
from .entry_blocks import BlockAddress, BlockReference, AnyAddress
from .bit_server_http_client import BitServerHTTPClient, DefaultBitServerAddressBase
from .store import StoreRef, Store


class BitServerStore(Store):
    def __init__(self, public, private, server):
        self.public = public
        self.private = private
        self.server = server
        pass

    def put(
        self, address: str, bs: bytes
    ) -> typing.Tuple[typing.Optional[StoreRef], typing.Optional[spin.Error]]:
        resp = self.server.ops(
            BitOpsRequest(
                public=self.public,
                private=self.private,
                ops=[BitOp(type=BitOpType.PutBitOp, address=address, bytes=bs)],
            )
        )
        if resp.error != "":
            return None, spin.error_from_string(resp.error)
        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return resp.outcomes[0].store_ref, None

    def get(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Tuple[
        typing.Optional[bytes], typing.Optional[StoreRef], typing.Optional[spin.Error]
    ]:
        resp = self.server.ops(
            BitOpsRequest(
                public=self.public,
                private=self.private,
                ops=[BitOp(type=BitOpType.GetBitOp, address=address, reference=ref)],
            )
        )
        if resp.error != "":
            return None, None, spin.error_from_string(resp.error)
        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return resp.outcomes[0].bytes, resp.outcomes[0].store_ref, None

    def delete(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Optional[spin.Error]:
        resp = self.server.ops(
            BitOpsRequest(
                public=self.public,
                private=self.private,
                ops=[BitOp(type=BitOpType.DelBitOp, address=address, reference=ref)],
            )
        )
        if resp.error != "":
            return spin.error_from_string(resp.error)
        if len(resp.outcomes) != 1:
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return None


class MuxStore(Store):
    def __init__(self, which_store):
        self.which_store = which_store

    def put(
        self, address: BlockAddress, bs: bytes
    ) -> typing.Tuple[typing.Optional[StoreRef], typing.Optional[spin.Error]]:
        s = self.which_store(address)
        return s.put(address, bs)

    def get(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Tuple[
        typing.Optional[bytes], typing.Optional[StoreRef], typing.Optional[spin.Error]
    ]:
        s = self.which_store(address)
        return s.get(address, ref)

    def delete(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Optional[spin.Error]:
        s = self.which_store(address)
        return s.delete(address, ref)


def _make_which_store(pu, pr, default_addr):
    """
    private helper function for store_for_citizen below.
    """
    stores = {}

    og_bs = BitServerHTTPClient(address=default_addr)

    def which(addr):
        if addr in stores:
            return stores[addr]

        if addr == AnyAddress or addr == default_addr:
            s = BitServerStore(pu, pr, og_bs)
        elif addr.startswith("https:"):
            bs = BitServerHTTPClient(address=addr)
            s = BitServerStore(pu, pr, bs)
        else:
            return None

        stores[addr] = s
        return s

    return which


def store_for_citizen(public, private, citizen):
    """
    Construct a data store which will correctly retrieve data from multiple addresses while
    also writing to the citizen's storage by default.
    """
    return MuxStore(
        _make_which_store(public, private, DefaultBitServerAddressBase + "/" + citizen)
    )
