# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class PackType(enum.Enum):
    MissingPackType = 0
    Dev1Pack = 1
    Dev2Pack = 2
    Dev3Pack = 3
    PlainPack = 4
    SHA256Pack = 5
    RSAWrapAESPack = 6
    OpaquePack = 7
