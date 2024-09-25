# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import spinsys.data as data
from .client import Client
from .options import Options

from spinsys._test_utils import (
    SPIN_PYTHON_TEST_PUBLIC,
    SPIN_PYTHON_TEST_PRIVATE,
    SPIN_PYTHON_TEST_CITIZEN,
)


def test_for_smoke():
    c = Client(
        Options(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            dir_server=data.DirServerHTTPClient(),
            store=data.store_for_citizen(
                SPIN_PYTHON_TEST_PUBLIC,
                SPIN_PYTHON_TEST_PRIVATE,
                SPIN_PYTHON_TEST_CITIZEN,
            ),
        )
    )

    fs = c.namespace(SPIN_PYTHON_TEST_CITIZEN).fs()

    resp = fs.ls("/")
    assert len(resp) >= 0

    fs.makedirs("/this/a/test")
    fs.rm_file("/this/a/test")
    fs.touch("/this/a/test.txt")

    assert fs.exists("/this/a/test.txt")
    assert fs.isfile("/this/a/test.txt")
    assert fs.cat("/this/a/test.txt") == b""

    fs.copy("/this/a/test.txt", "/this/a/copy.txt")
    out = {x: True for x in fs.ls("/this/a", detail=False)}

    assert "/this/a/test.txt" in out, f"out was {out}"
    assert "/this/a/copy.txt" in out, f"out was {out}"

    fs.rm("/this", recursive=True)

    fs.listdir("/")
    fs.ls("/")


def test_namespace_open():
    c = Client(
        Options(
            public=SPIN_PYTHON_TEST_PUBLIC,
            private=SPIN_PYTHON_TEST_PRIVATE,
            dir_server=data.DirServerHTTPClient(),
            store=data.store_for_citizen(
                SPIN_PYTHON_TEST_PUBLIC,
                SPIN_PYTHON_TEST_PRIVATE,
                SPIN_PYTHON_TEST_CITIZEN,
            ),
        )
    )

    fs = c.namespace(SPIN_PYTHON_TEST_CITIZEN).fs()

    fs.touch("/test.txt")

    fs.ns.open("/test.txt").read()
