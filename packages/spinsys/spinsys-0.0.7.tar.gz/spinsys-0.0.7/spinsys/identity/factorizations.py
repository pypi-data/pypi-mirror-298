# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses

from .factorization_types import FactorizationType
from .factors import Factor


@dataclasses.dataclass
class Factorization:
    """
    Factorization is a helper class for a spin factorization.
    """

    type: FactorizationType = FactorizationType.MissingFactorizationType
    factors: list[Factor] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_json(j: dict) -> "Factorization":
        f = Factorization()
        f.unmarshal_json(j)
        return f

    def unmarshal_json(self, j: dict):
        if "Type" in j:
            self.type = FactorizationType(j["Type"])
        if "Factors" in j and j["Factors"] is not None:
            self.factors = [Factor.from_json(f) for f in j["Factors"]]

    def to_json(self) -> dict:
        j: dict = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["Type"] = self.type
        j["Factors"] = [f.to_json() for f in self.factors]
