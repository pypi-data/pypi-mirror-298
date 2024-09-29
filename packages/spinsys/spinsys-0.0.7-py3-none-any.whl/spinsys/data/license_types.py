# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class LicenseType(enum.Enum):
    MissingLicenseType = 0
    Dev1License = 1
    Dev2License = 2
    Dev3License = 3
    InheritLicense = 4
    ReplaceLicense = 5
    OpaqueLicense = 6
