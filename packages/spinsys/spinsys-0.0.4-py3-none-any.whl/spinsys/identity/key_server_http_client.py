# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import requests

from .key_server import KeyAuthRequest, KeyAuthResponse

"""
    DefaultKeyProtocolVersion is the default key protocol version
    used by the KeyServerHTTPClient class.
"""
DefaultKeyProtocolVersion = "v0.0.0"

""" 
    DefaultKeyServerAddress is the default key server address
    used by the KeyServerHTTPClient class.
"""
DefaultKeyServerAddress = "https://keys-ddh4amviaq-uw.a.run.app"


class KeyServerHTTPClient(object):
    """
    KeyServerHTTPClient is a helper class for a key server HTTP client.
    """

    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: str = DefaultKeyServerAddress,
        protocol: str = DefaultKeyProtocolVersion,
    ):
        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def auth(self, req: KeyAuthRequest) -> KeyAuthResponse:
        if self.debug:
            print(f"KeyServerHTTPClient.auth {req}")

        url = self.address + "/" + self.protocol + "/auth"
        return KeyAuthResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
