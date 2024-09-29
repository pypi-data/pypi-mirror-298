# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import hashlib


def sha256(b: bytes):
    """
    SHA256 creates a sum of the data
    """

    m = hashlib.sha256()
    m.update(b)
    return m.hexdigest()
