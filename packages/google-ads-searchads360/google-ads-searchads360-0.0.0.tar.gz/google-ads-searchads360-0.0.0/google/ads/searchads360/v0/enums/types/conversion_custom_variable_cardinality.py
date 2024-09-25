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
        'ConversionCustomVariableCardinalityEnum',
    },
)


class ConversionCustomVariableCardinalityEnum(proto.Message):
    r"""Container for enum describing the family of a conversion
    custom variable.

    """
    class ConversionCustomVariableCardinality(proto.Enum):
        r"""Cardinality of a conversion custom variable."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        BELOW_ALL_LIMITS = 2
        EXCEEDS_SEGMENTATION_LIMIT_BUT_NOT_STATS_LIMIT = 3
        APPROACHES_STATS_LIMIT = 4
        EXCEEDS_STATS_LIMIT = 5


__all__ = tuple(sorted(__protobuf__.manifest))
