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
        'AdGroupAdEngineStatusEnum',
    },
)


class AdGroupAdEngineStatusEnum(proto.Message):
    r"""Container for enum describing possible AdGroupAd engine
    statuses.

    """
    class AdGroupAdEngineStatus(proto.Enum):
        r"""Enumerates AdGroupAd engine statuses."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_AD_ELIGIBLE = 2
        AD_GROUP_AD_INAPPROPRIATE_FOR_CAMPAIGN = 3
        AD_GROUP_AD_MOBILE_URL_UNDER_REVIEW = 4
        AD_GROUP_AD_PARTIALLY_INVALID = 5
        AD_GROUP_AD_TO_BE_ACTIVATED = 6
        AD_GROUP_AD_NOT_REVIEWED = 7
        AD_GROUP_AD_ON_HOLD = 8
        AD_GROUP_AD_PAUSED = 9
        AD_GROUP_AD_REMOVED = 10
        AD_GROUP_AD_PENDING_REVIEW = 11
        AD_GROUP_AD_UNDER_REVIEW = 12
        AD_GROUP_AD_APPROVED = 13
        AD_GROUP_AD_DISAPPROVED = 14
        AD_GROUP_AD_SERVING = 15
        AD_GROUP_AD_ACCOUNT_PAUSED = 16
        AD_GROUP_AD_CAMPAIGN_PAUSED = 17
        AD_GROUP_AD_AD_GROUP_PAUSED = 18


__all__ = tuple(sorted(__protobuf__.manifest))
