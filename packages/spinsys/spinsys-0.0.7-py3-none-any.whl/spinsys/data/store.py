# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import abc
import dataclasses
import typing

import spinsys.spin as spin
from .entry_blocks import BlockAddress, BlockReference


@dataclasses.dataclass
class StoreRef:
    address: BlockAddress = ""
    reference: BlockReference = ""
    volatile: bool = False
    expires_at: spin.Time = 0

    @staticmethod
    def from_json(j: dict):
        r = StoreRef()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Address" in j:
            self.address = j["Address"]
        if "Reference" in j:
            self.reference = j["Reference"]
        if "Volatile" in j:
            self.volatile = j["Volatile"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Address"] = self.address
        j["Reference"] = self.reference
        j["Volatile"] = self.volatile
        j["ExpiresAt"] = self.expires_at


class Store(abc.ABC):
    @abc.abstractmethod
    def put(
        self, address: BlockAddress, bs: bytes
    ) -> tuple[typing.Optional[StoreRef], typing.Optional[spin.Error]]:
        pass

    @abc.abstractmethod
    def get(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Tuple[
        typing.Optional[bytes], typing.Optional[StoreRef], typing.Optional[spin.Error]
    ]:
        pass

    @abc.abstractmethod
    def delete(
        self, address: BlockAddress, ref: BlockReference
    ) -> typing.Optional[spin.Error]:
        pass
