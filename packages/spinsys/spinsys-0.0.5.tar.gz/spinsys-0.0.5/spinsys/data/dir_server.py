# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses

import spinsys.spin as spin
from .dir_ops import DirOp
from .entries import Entry
from .entry_levels import EntryLevel
from .path_patterns import PathPattern


@dataclasses.dataclass
class DirApplyRequest:
    public: str = ""
    private: str = ""
    ops: list[DirOp] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict):
        r = DirApplyRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Ops" in j and j["Ops"] is not None:
            self.ops = [DirOp.from_json(op) for op in j["Ops"]]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Ops"] = [op.to_json() for op in self.ops]


@dataclasses.dataclass
class DirApplyResponse:
    entries: list[Entry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirApplyResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [Entry.from_json(op) for op in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Entries"] = [op.to_json() for op in self.entries]
        j["Error"] = self.error


@dataclasses.dataclass
class DirListRequest:
    public: str = ""
    private: str = ""
    citizen: spin.Name = ""
    path: spin.Path = ""
    level: EntryLevel = 0
    pattern: PathPattern = ""

    @staticmethod
    def from_json(j: dict):
        r = DirListRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Path" in j:
            self.path = j["Path"]
        if "Level" in j:
            self.level = j["Level"]
        if "Pattern" in j:
            self.pattern = j["Pattern"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Public"] = self.public
        j["Private"] = self.private
        j["Citizen"] = self.citizen
        j["Path"] = self.path
        j["Level"] = self.level
        j["Pattern"] = self.pattern


@dataclasses.dataclass
class DirListResponse:
    entries: list[Entry] = dataclasses.field(default_factory=list)
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        r = DirListResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Entries" in j and j["Entries"] is not None:
            self.entries = [Entry.from_json(op) for op in j["Entries"]]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Entries"] = [op.to_json() for op in self.entries]
        j["Error"] = self.error
