# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import requests

from .dir_server import (
    DirApplyRequest,
    DirApplyResponse,
    DirListRequest,
    DirListResponse,
)

"""
    DefaultDirProtocolVersion is the default dir protocol version
    used by the DirServerHTTPClient class.
"""
DefaultDirProtocolVersion = "v0.0.0"

"""
    DefaultDirServerAddress is the default dir server address
    used by the DirServerHTTPClient class.
"""
DefaultDirServerAddress = "https://dirs-ddh4amviaq-uw.a.run.app"


class DirServerHTTPClient(object):
    """
    DirServerHTTPClient is a helper class for a dir server HTTP client.
    """

    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: str = DefaultDirServerAddress,
        protocol: str = DefaultDirProtocolVersion,
    ):
        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def apply(self, req: DirApplyRequest):
        if self.debug:
            print(f"DirServerHTTPClient.apply {req}")

        url = self.address + "/" + self.protocol + "/apply"
        return DirApplyResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )

    def list(self, req: DirListRequest):
        if self.debug:
            print(f"DirServerHTTPClient.list {req}")

        url = self.address + "/" + self.protocol + "/list"
        return DirListResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
