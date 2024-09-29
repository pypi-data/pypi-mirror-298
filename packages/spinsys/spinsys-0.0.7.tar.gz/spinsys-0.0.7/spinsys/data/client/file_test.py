# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import os
import tempfile
import shutil

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

    f = fs.open("/notes.txt", "wb")
    f.write(b"Hello world!")
    f.close()
    f = fs.open("/notes.txt", "rb")
    b = f.read()
    assert b == b"Hello world!", f"got {b}, wanted Hello world!"
    fs.rm("/notes.txt")


def create_large_temp_file(size_mb=11):
    """
    Create a temporary file of a given size in MB
    """
    # Convert MB to bytes
    size_bytes = size_mb * 1024 * 1024

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write random data to the file
        temp_file.write(os.urandom(size_bytes))

        # Get the file path
        file_path = temp_file.name

    # Return the path of the created file
    return file_path


def test_large_upload():
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

    fp = create_large_temp_file(size_mb=21)

    src = open(fp, "rb")
    dst = fs.open("/test.mp4", "wb")
    shutil.copyfileobj(src, dst)
    src.close()
    dst.close()

    b = fs.open("/test.mp4", "rb").read()

    # check that b is the same as the original file
    assert b == open(fp, "rb").read()

    resp = fs.rm("/test.mp4")
    assert resp is None

    os.remove(fp)
