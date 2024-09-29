# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses
import typing

import spinsys.spin as spin
from spinsys.identity import Proxy  # to avoid collision with identity field
from .permission_grant_types import PermissionGrantType
from .permissions import Permissions


@dataclasses.dataclass
class PermissionGrant:
    uuid: typing.Union[spin.UUID, None] = None
    path: spin.Path = ""
    type: PermissionGrantType = PermissionGrantType.MissingPermissionGrantType
    identity: Proxy = dataclasses.field(default_factory=Proxy)
    permissions: Permissions = 0
    expires_at: spin.Time = 0
    created_at: spin.Time = 0
    created_by: Proxy = dataclasses.field(default_factory=Proxy)

    @staticmethod
    def from_json(j: dict):
        g = PermissionGrant()
        g.unmarshal_json(j)
        return g

    def unmarshal_json(self, j: dict):
        if "UUID" in j:
            self.uuid = spin.UUID(j["UUID"])
        if "Path" in j:
            self.path = j["Path"]
        if "Type" in j:
            self.type = PermissionGrantType(j["Type"])
        if "Identity" in j:
            self.identity = Proxy.from_json(j["Identity"])
        if "Permissions" in j:
            self.permissions = j["Permissions"]
        if "ExpiresAt" in j:
            self.expires_at = j["ExpiresAt"]
        if "CreatedAt" in j:
            self.created_at = j["CreatedAt"]
        if "CreatedBy" in j:
            self.created_by = Proxy.from_json(j["CreatedBy"])

    def to_json(self):
        j = {}
        self.marshal_json(j)
        return j

    def marshal_json(self, j: dict):
        j["UUID"] = str(self.uuid)
        j["Path"] = self.path
        j["Type"] = self.type.value
        j["Identity"] = self.identity.to_json()
        j["Permissions"] = self.permissions
        j["ExpiresAt"] = self.expires_at
        j["CreatedAt"] = self.created_at
        j["CreatedBy"] = self.created_by.to_json()
