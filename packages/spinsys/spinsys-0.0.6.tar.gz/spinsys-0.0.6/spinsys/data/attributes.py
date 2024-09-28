# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses


@dataclasses.dataclass
class Attribute:
    name: str = ""
    data: str = ""

    @staticmethod
    def from_json(j: dict):
        a = Attribute()
        a.unmarshal_json(j)
        return a

    def unmarshal_json(self, j: dict):
        if "Name" in j:
            self.name = j["Name"]
        if "Data" in j:
            self.data = j["Data"]

    def to_json(self):
        j = {}
        return self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Name"] = self.name
        j["Data"] = self.data
