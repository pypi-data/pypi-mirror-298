# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import typing

import requests

from .bit_server import BitOpsRequest, BitOpsResponse


""" 
    DefaultBitProtocolVersion is the default bit protocol version
    used by the BitServerHTTPClient class.
"""
DefaultBitProtocolVersion = "v0.0.0"

"""
    DefaultBitServerAddressBase is the default bit server address
    used by the BitServerHTTPClient class.
"""
DefaultBitServerAddressBase = "https://bits-ddh4amviaq-uw.a.run.app"


class BitServerHTTPClient(object):
    """
    BitServerHTTPClient is a helper class for a bit server HTTP client.
    """

    def __init__(
        self,
        session=requests.Session(),
        debug: bool = False,
        address: typing.Optional[str] = None,
        protocol: str = DefaultBitProtocolVersion,
    ):
        if not address:
            raise ValueError("address must be specified")

        self.address = address
        self.protocol = protocol
        self.session = session
        self.debug = debug

    def ops(self, req: BitOpsRequest, address=None):
        if self.debug:
            print(f"BitServerHTTPClient.ops {req}")
        if address is None or address == "":
            address = self.address

        url = address + "/" + self.protocol + "/ops"
        resp = BitOpsResponse.from_json(
            self.session.post(url, json=req.to_json()).json()
        )
        for out in resp.outcomes:
            if out.store_ref.address == "":
                out.store_ref.address = address
        return resp
