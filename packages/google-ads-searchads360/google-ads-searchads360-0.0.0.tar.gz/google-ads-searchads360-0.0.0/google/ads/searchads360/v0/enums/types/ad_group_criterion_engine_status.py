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
        'AdGroupCriterionEngineStatusEnum',
    },
)


class AdGroupCriterionEngineStatusEnum(proto.Message):
    r"""Container for enum describing possible AdGroupCriterion
    engine statuses.

    """
    class AdGroupCriterionEngineStatus(proto.Enum):
        r"""Enumerates AdGroupCriterion engine statuses."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_CRITERION_ELIGIBLE = 2
        AD_GROUP_CRITERION_INAPPROPRIATE_FOR_CAMPAIGN = 3
        AD_GROUP_CRITERION_INVALID_MOBILE_SEARCH = 4
        AD_GROUP_CRITERION_INVALID_PC_SEARCH = 5
        AD_GROUP_CRITERION_INVALID_SEARCH = 6
        AD_GROUP_CRITERION_LOW_SEARCH_VOLUME = 7
        AD_GROUP_CRITERION_MOBILE_URL_UNDER_REVIEW = 8
        AD_GROUP_CRITERION_PARTIALLY_INVALID = 9
        AD_GROUP_CRITERION_TO_BE_ACTIVATED = 10
        AD_GROUP_CRITERION_UNDER_REVIEW = 11
        AD_GROUP_CRITERION_NOT_REVIEWED = 12
        AD_GROUP_CRITERION_ON_HOLD = 13
        AD_GROUP_CRITERION_PENDING_REVIEW = 14
        AD_GROUP_CRITERION_PAUSED = 15
        AD_GROUP_CRITERION_REMOVED = 16
        AD_GROUP_CRITERION_APPROVED = 17
        AD_GROUP_CRITERION_DISAPPROVED = 18
        AD_GROUP_CRITERION_SERVING = 19
        AD_GROUP_CRITERION_ACCOUNT_PAUSED = 20


__all__ = tuple(sorted(__protobuf__.manifest))
