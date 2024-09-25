# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class KeyType(enum.Enum):
    """
    KeyType is a helper type for a key's type.
    """

    MissingKeyType = 0
    Dev1Key = 1
    Dev2Key = 2
    Dev3Key = 3
    BcryptPasswordKey = 4
    RSAPublicKey = 5
