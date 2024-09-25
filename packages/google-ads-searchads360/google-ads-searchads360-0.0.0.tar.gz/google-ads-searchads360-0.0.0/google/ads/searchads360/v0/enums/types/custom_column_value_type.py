# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.enums',
    marshal='google.ads.searchads360.v0',
    manifest={
        'CustomColumnValueTypeEnum',
    },
)


class CustomColumnValueTypeEnum(proto.Message):
    r"""The value type of custom columns.
    """
    class CustomColumnValueType(proto.Enum):
        r"""Enum containing possible custom column value types."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        STRING = 2
        INT64 = 3
        DOUBLE = 4
        BOOLEAN = 5
        DATE = 6


__all__ = tuple(sorted(__protobuf__.manifest))
