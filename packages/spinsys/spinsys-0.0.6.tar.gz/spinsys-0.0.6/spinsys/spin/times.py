# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import datetime

"""
    Time represents a timestamp, in units of *micro*seconds,
    since the Unix epoch, Jan 1 1970 0:00 UTC.
"""
Time = int


def now() -> Time:
    """
    Returns the current time as a spin Time.
    """
    return time_from_python(datetime.datetime.now(tz=datetime.timezone.utc))


def python_time(t: Time) -> datetime.datetime:
    """
    Converts a spin Time to a Python datetime object.
    """
    return datetime.datetime.fromtimestamp(t / 1_000_000, tz=datetime.timezone.utc)


def time_from_python(t: datetime.datetime) -> Time:
    """
    Converts a Python datetime object to a spin Time.
    """
    return int(t.timestamp() * 1_000_000)
