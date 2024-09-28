# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses

from .bit_ops import BitOp, BitOpOutcome


@dataclasses.dataclass
class BitOpsRequest:
    public: str = ""
    private: str = ""
    ops: list[BitOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = BitOpsRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [BitOp.from_json(op) for op in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [op.to_json() for op in self.ops]


@dataclasses.dataclass
class BitOpsResponse:
    outcomes: list[BitOpOutcome] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = BitOpsResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Outcomes" in j and j["Outcomes"] is not None:
            self.outcomes = [BitOpOutcome.from_json(op) for op in j["Outcomes"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Outcomes"] = [op.to_json() for op in self.outcomes]
        j["Error"] = self.error
