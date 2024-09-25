# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

# Path represents a spin path.
Path = str


def path_ancestors(p: Path) -> list[Path]:
    """
    path_ancestors returns the paths of the ancestors, in order.
    The root path has no ancestors, and so the returned slice may be empty.
    The path is not checked to be valid.
    """

    if p == "":
        raise Exception("path_ancestors given empty path")

    if p == "/":
        return []

    rest = p[1:]
    # count number of slashes
    c = p.count("/")
    ancestors = [""] * c
    for i in range(1, c):
        j = rest.find("/")
        ancestors[i] = ancestors[i - 1] + "/" + rest[:j]  # exclude ending slash
        rest = rest[j + 1 :]  # exclude leading slash
    ancestors[0] = "/"
    return ancestors


def path_is_ancestor(a: Path, p: Path) -> bool:
    """
    path_is_ancestor determines if a is an ancestor of p.
    """
    return p != a and p.startswith(a)


_root_sequence = ["/"]  # for path_sequence


def path_sequence(p: Path) -> list[Path]:
    """
    path_sequence returns a list of paths from (and including) the root to (and
    including) p.
    """

    if p == "":
        raise Exception("path_sequence given empty path")

    if p == "/":
        return _root_sequence

    ancestors = path_ancestors(p)
    ancestors.append(p)
    return ancestors
