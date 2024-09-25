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


def test_dir_http_client_for_smoke():
    client = data.DirServerHTTPClient()
    resp = client.list(data.DirListRequest(public="lando", private="random"))
    assert resp.error == spin.ErrNotVerified


def test_with_credentials():
    dc = data.DirServerHTTPClient()
    resp = dc.list(
        data.DirListRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            citizen=SPIN_PYTHON_TEST_CITIZEN,
            path="/",
            level=0,
        )
    )
    assert resp.error == ""
    assert len(resp.entries) == 1

    resp = dc.list(
        data.DirListRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            citizen=SPIN_PYTHON_TEST_CITIZEN,
            path="/",
            level=1,
        )
    )
    assert resp.error == ""

    resp = dc.apply(
        data.DirApplyRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            ops=[
                data.DirOp(
                    type=data.DirOpType.PutDirOp,
                    entry=data.Entry(
                        type=data.EntryType.DirectoryEntry,
                        citizen=SPIN_PYTHON_TEST_CITIZEN,
                        path="/test",
                        version=data.IgnoreVersion,
                    ),
                )
            ],
        )
    )
    assert resp.error == ""
    assert len(resp.entries) == 1

    resp = dc.apply(
        data.DirApplyRequest(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            ops=[
                data.DirOp(
                    type=data.DirOpType.DelDirOp,
                    entry=data.Entry(
                        type=data.EntryType.DirectoryEntry,
                        citizen=SPIN_PYTHON_TEST_CITIZEN,
                        path="/test",
                        version=resp.entries[0].version,
                    ),
                )
            ],
        )
    )
    assert resp.error == ""
    assert len(resp.entries) == 1
