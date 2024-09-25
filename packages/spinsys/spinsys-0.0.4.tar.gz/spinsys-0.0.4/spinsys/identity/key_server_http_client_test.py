# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import spinsys.identity as identity
from spinsys._test_utils import (
    SPIN_PYTHON_TEST_PUBLIC,
    SPIN_PYTHON_TEST_PRIVATE,
    SPIN_PYTHON_TEST_CITIZEN,
)


def test_key_http_client():
    client = identity.KeyServerHTTPClient()
    resp = client.auth(
        identity.KeyAuthRequest(public="lando", private="random", nonce="random")
    )
    assert resp.error == ""
    assert resp.nonce == "random"


def test_with_credentials():
    kc = identity.KeyServerHTTPClient()
    n = identity.new_nonce(16)
    resp = kc.auth(
        identity.KeyAuthRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            duration=600,
            nonce=n,
        )
    )

    assert resp.error == ""
    assert resp.nonce == n
    assert resp.key.citizen == SPIN_PYTHON_TEST_CITIZEN
