# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses


@dataclasses.dataclass
class Attribute:
    key: str = ""
    value: str = ""

    @staticmethod
    def from_json(j: dict):
        a = Attribute()
        a.unmarshal_json(j)
        return a

    def unmarshal_json(self, j: dict):
        if "Key" in j:
            self.key = j["Key"]
        if "Value" in j:
            self.value = j["Value"]

    def to_json(self):
        j = {}
        return self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Key"] = self.key
        j["Value"] = self.value
