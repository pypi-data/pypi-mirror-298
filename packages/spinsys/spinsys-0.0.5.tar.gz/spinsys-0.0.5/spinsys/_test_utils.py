# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import os

if "SPIN_PYTHON_TEST_PUBLIC" not in os.environ:
    raise ValueError("must specify SPIN_PYTHON_TEST_PUBLIC environment variable")

if "SPIN_PYTHON_TEST_PRIVATE" not in os.environ:
    raise ValueError("must specify SPIN_PYTHON_TEST_PRIVATE environment variable")

if "SPIN_PYTHON_TEST_CITIZEN" not in os.environ:
    raise ValueError("must specify SPIN_PYTHON_TEST_CITIZEN environment variable")

SPIN_PYTHON_TEST_PUBLIC = os.environ["SPIN_PYTHON_TEST_PUBLIC"]
SPIN_PYTHON_TEST_PRIVATE = os.environ["SPIN_PYTHON_TEST_PRIVATE"]
SPIN_PYTHON_TEST_CITIZEN = os.environ["SPIN_PYTHON_TEST_CITIZEN"]
