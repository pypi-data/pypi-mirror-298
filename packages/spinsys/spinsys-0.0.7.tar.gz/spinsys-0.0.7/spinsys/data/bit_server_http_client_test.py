# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import spinsys.spin as spin
import spinsys.data as data
from spinsys._test_utils import (
    SPIN_PYTHON_TEST_PUBLIC,
    SPIN_PYTHON_TEST_PRIVATE,
    SPIN_PYTHON_TEST_CITIZEN,
)


def test_bit_http_client_for_smoke():
    client = data.BitServerHTTPClient(
        address=data.DefaultBitServerAddressBase + "/lando"
    )
    resp = client.ops(data.BitOpsRequest(public="lando", private="random"))
    assert resp.error == spin.ErrNotVerified


def test_with_credentials():
    bc = data.BitServerHTTPClient(
        address=data.DefaultBitServerAddressBase + "/" + SPIN_PYTHON_TEST_CITIZEN
    )
    bs = "asdf some data".encode()
    resp = bc.ops(
        data.BitOpsRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            ops=[
                data.BitOp(
                    type=data.BitOpType.PutBitOp,
                    address=data.AnyAddress,
                    reference=data.sha256(bs),
                    bytes=bs,
                )
            ],
        )
    )
    assert resp.error == ""
    assert len(resp.outcomes) == 1
    assert resp.outcomes[0].store_ref.reference == data.sha256(bs)
