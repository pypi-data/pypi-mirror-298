# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses
import typing


import spinsys.spin as spin
from .keys import (
    Key,
    PrivateKey,
)
from .factor_server import (
    FactorChallengeResponse,
    FactorVerifyResponse,
)


@dataclasses.dataclass
class KeyAuthRequestFactor:
    """
    KeyAuthRequestFactor is a helper class for a spin key auth request factor.
    """

    public: str = ""
    private: str = ""

    @staticmethod
    def from_json(j: dict):
        f = KeyAuthRequestFactor()
        f.unmarshal_json(j)
        return f

    def unmarshal_json(self, j: dict):
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Public"] = self.public
        j["Private"] = self.private
        return j


@dataclasses.dataclass
class KeyAuthRequest:
    """
    KeyAuthRequest is a helper class for a spin key auth request.
    """

    nonce: str = ""
    public: str = ""
    private: str = ""
    factors: list[KeyAuthRequestFactor] = dataclasses.field(default_factory=list)
    duration: int = 0  # microseconds
    derived_name: str = ""
    derived_alias: str = ""
    derived_type: int = 0
    derived_data: str = ""

    @staticmethod
    def from_json(j: dict):
        r = KeyAuthRequest()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "Public" in j:
            self.public = j["Public"]
        if "Private" in j:
            self.private = j["Private"]
        if "Factors" in j and j["Factors"] is not None:
            self.blocks = [KeyAuthRequestFactor.from_json(f) for f in j["Factors"]]
        if "Duration" in j:
            self.duration = j["Duration"]
        if "DerivedName" in j:
            self.derived_name = j["DerivedName"]
        if "DerivedAlias" in j:
            self.derived_alias = j["DerivedAlias"]
        if "DerivedType" in j:
            self.derived_type = j["DerivedType"]
        if "DerivedData" in j:
            self.derived_data = j["DerivedData"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["Public"] = self.public
        j["Private"] = self.private
        j["Factors"] = [f.to_json() for f in self.factors]
        j["Duration"] = self.duration
        j["DerivedName"] = self.derived_name
        j["DerivedAlias"] = self.derived_alias
        j["DerivedType"] = self.derived_type
        j["DerivedData"] = self.derived_data
        return j


@dataclasses.dataclass
class KeyAuthResponse:
    """
    KeyAuthResponse is a helper class for a spin key auth response.
    """

    nonce: str = ""
    handled_at: spin.Time = 0
    key_verified: bool = False
    key: typing.Optional[Key] = None
    derived: typing.Optional[PrivateKey] = None
    factor_challenges: list[FactorChallengeResponse] = dataclasses.field(
        default_factory=list
    )
    factor_verifies: list[FactorVerifyResponse] = dataclasses.field(
        default_factory=list
    )
    error: str = ""

    @staticmethod
    def from_json(j: dict):
        print(j)
        r = KeyAuthResponse()
        r.unmarshal_json(j)
        return r

    def unmarshal_json(self, j: dict):
        if "Nonce" in j:
            self.nonce = j["Nonce"]
        if "HandledAt" in j:
            self.handled_at = j["HandledAt"]
        if "KeyVerified" in j:
            self.key_verified = j["KeyVerified"]
        if "Key" in j and j["Key"] is not None:
            self.key = Key.from_json(j["Key"])
        if "Derived" in j and j["Derived"] is not None:
            print("here")
            self.derived = PrivateKey.from_json(j["Derived"])
        if "FactorChallenges" in j and j["FactorChallenges"] is not None:
            self.factor_challenges = [
                FactorChallengeResponse.from_json(f) for f in j["FactorChallenges"]
            ]
        if "FactorVerifies" in j and j["FactorVerifies"] is not None:
            self.factor_verifies = [
                FactorVerifyResponse.from_json(f) for f in j["FactorVerifies"]
            ]
        if "Error" in j:
            self.error = j["Error"]

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j):
        j["Nonce"] = self.nonce
        j["HandledAt"] = self.handled_at
        j["KeyVerified"] = self.key_verified
        j["Key"] = self.key.to_json()
        j["Derived"] = self.derived.to_json()
        j["FactorChallenges"] = [f.to_json() for f in self.factor_challenges]
        j["FactorVerifies"] = [f.to_json() for f in self.factor_verifies]
        j["Error"] = self.error
        return j
