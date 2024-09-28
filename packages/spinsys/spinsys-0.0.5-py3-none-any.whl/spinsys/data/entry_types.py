# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import enum


class EntryType(enum.Enum):
    MissingEntryType = 0
    Dev1Entry = 1
    Dev2Entry = 2
    Dev3Entry = 3
    DirectoryEntry = 4
    FileEntry = 5
