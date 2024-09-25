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
        'AccountTypeEnum',
    },
)


class AccountTypeEnum(proto.Message):
    r"""Container for enum describing engine account types.
    """
    class AccountType(proto.Enum):
        r"""Possible engine account types."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        BAIDU = 2
        ENGINE_TRACK = 3
        FACEBOOK = 4
        FACEBOOK_GATEWAY = 5
        GOOGLE_ADS = 6
        MICROSOFT = 7
        SEARCH_ADS_360 = 8
        YAHOO_JAPAN = 9


__all__ = tuple(sorted(__protobuf__.manifest))
