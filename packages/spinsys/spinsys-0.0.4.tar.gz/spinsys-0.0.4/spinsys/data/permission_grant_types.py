# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class PermissionGrantType(enum.Enum):
    MissingPermissionGrantType = 0
    Dev1PermissionGrant = 1
    Dev2PermissionGrant = 2
    Dev3PermissionGrant = 3
    InherentGrant = 4
    OpaqueGrant = 5
    IdentityGrant = 11
    AliasPathGrant = 12
