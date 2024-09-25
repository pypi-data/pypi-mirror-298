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
        'CustomColumnRenderTypeEnum',
    },
)


class CustomColumnRenderTypeEnum(proto.Message):
    r"""The render type of custom columns.
    """
    class CustomColumnRenderType(proto.Enum):
        r"""Enum containing the different ways a custom column can be
        interpreted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NUMBER = 2
        PERCENT = 3
        MONEY = 4
        STRING = 5
        BOOLEAN = 6
        DATE = 7


__all__ = tuple(sorted(__protobuf__.manifest))
