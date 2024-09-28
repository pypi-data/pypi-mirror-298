# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class FactorizationType(enum.Enum):
    """
    FactorizationType indicates the type of a key factorization.
    """

    MissingFactorizationType = 0
    Dev1Factorization = 1
    Dev2Factorization = 2
    Dev3Factorization = 3
    NeedsAllFactors = 4
    NeedsAnyOneFactor = 5
