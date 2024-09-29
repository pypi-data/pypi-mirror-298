# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses
import enum

from .entries import Entry


class DirOpType(enum.Enum):
    MissingDirOpType = 0
    Dev1DirOp = 1
    Dev2DirOp = 2
    Dev3DirOp = 3
    PutDirOp = 4
    DelDirOp = 5
    ApdDirOp = 6
    LicDirOp = 7


@dataclasses.dataclass
class DirOp:
    type: DirOpType = DirOpType.MissingDirOpType
    entry: Entry = dataclasses.field(default_factory=Entry)

    @staticmethod
    def from_json(j: dict):
        o = DirOp()
        o.unmarshal_json(j)
        return o

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = DirOpType(j["Type"])
        if "Entry" in j:
            self.entry = Entry.from_json(j["Entry"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type.value
        j["Entry"] = self.entry.to_json()
