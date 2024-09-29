# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import os
import binascii


def new_nonce(length: int) -> str:
    """
    Creates a nonce of the specified number of bytes.
    The returned string is encoded in hex.
    Consequently, it will be 2*length ASCII characters.

    Args:
        length (int): The number of bytes for the nonce.

    Returns:
        str: The nonce as a hex-encoded string.

    Raises:
        OSError: If there's an error reading random data.
    """
    try:
        nonce = os.urandom(length)
        return binascii.hexlify(nonce).decode("ascii")
    except OSError as e:
        raise OSError(f"Error reading random data: {e}")
