# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import uuid

import spinsys.identity as identity


def test_for_smoke():
    k = identity.Key()
    k.uuid = uuid.uuid4()
