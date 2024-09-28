# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses

import spinsys.spin as spin

# Alias represents a spin alias.
Alias = str


@dataclasses.dataclass
class Proxy:
    """
    Proxy is a helper type for a spin proxy identity.
    """

    citizen: spin.Name = ""
    alias: Alias = ""

    @staticmethod
    def from_json(j: dict):
        p = Proxy()
        p.unmarshal_json(j)
        return p

    def unmarshal_json(self, j: dict):
        if "Citizen" in j:
            self.citizen = j["Citizen"]
        if "Alias" in j:
            self.alias = j["Alias"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Citizen"] = self.citizen
        j["Alias"] = self.alias
