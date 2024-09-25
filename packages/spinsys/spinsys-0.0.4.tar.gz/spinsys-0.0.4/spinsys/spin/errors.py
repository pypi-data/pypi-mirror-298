# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

# Error represents a spin error.
Error = str

# Some standard errors.
ErrNotImplemented: Error = "not implemented"
ErrInternal: Error = "internal"
ErrNotFound: Error = "not found"
ErrExpired: Error = "expired"
ErrNotVerified: Error = "not verified"
ErrNotAuthorized: Error = "not authorized"


def error_from_string(s: str) -> Error:
    """
    error_from_string converses an error string to an Error.
    """

    if s == ErrNotImplemented:
        return ErrNotImplemented
    elif s == ErrInternal:
        return ErrInternal
    elif s == ErrNotFound:
        return ErrNotFound
    elif s == ErrExpired:
        return ErrExpired
    elif s == ErrNotVerified:
        return ErrNotVerified
    elif s == ErrNotAuthorized:
        return ErrNotAuthorized
    else:
        return Error(s)
