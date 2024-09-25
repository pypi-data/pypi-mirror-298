# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class FactorType(enum.Enum):
    """
    FactorType is a helper type for a factor's type.
    """

    MissingFactorType = 0
    Dev1Factor = 1
    Dev2Factor = 2
    Dev3Factor = 3
    BcryptPasswordFactor = 4
    RSAPublicKeyFactor = 5
    EmailCodeFactor = 6
    PhoneSMSCodeFactor = 7
