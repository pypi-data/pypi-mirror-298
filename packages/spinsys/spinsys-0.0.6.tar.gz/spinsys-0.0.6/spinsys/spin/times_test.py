# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

from .times import now, python_time, time_from_python


def test_times():
    t = now()
    assert t == time_from_python(python_time(t))
