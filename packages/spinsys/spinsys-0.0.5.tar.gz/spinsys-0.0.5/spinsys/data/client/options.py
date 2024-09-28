# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import dataclasses
import typing

import spinsys.spin as spin
import spinsys.data as data


@dataclasses.dataclass
class Options:
    """
    Options for a client.
    """

    public: str = ""

    private: str = ""

    dir_server: typing.Optional[data.DirServerHTTPClient] = data.DirServerHTTPClient()

    store: typing.Optional[data.Store] = None

    pack_type: data.PackType = data.PackType.MissingPackType

    block_size: int = 10 * 2**20

    get_time: typing.Callable[[], spin.Time] = spin.now
