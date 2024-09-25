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

from google.ads.searchads360.v0.enums.types import ad_group_ad_engine_status
from google.ads.searchads360.v0.enums.types import ad_group_ad_status
from google.ads.searchads360.v0.resources.types import ad as gasr_ad


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AdGroupAd',
    },
)


class AdGroupAd(proto.Message):
    r"""An ad group ad.
    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad. Ad group ad resource
            names have the form:

            ``customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}``
        status (google.ads.searchads360.v0.enums.types.AdGroupAdStatusEnum.AdGroupAdStatus):
            The status of the ad.
        ad (google.ads.searchads360.v0.resources.types.Ad):
            Immutable. The ad.
        creation_time (str):
            Output only. The timestamp when this ad_group_ad was
            created. The datetime is in the customer's time zone and in
            "yyyy-MM-dd HH:mm:ss.ssssss" format.
        labels (MutableSequence[str]):
            Output only. The resource names of labels
            attached to this ad group ad.
        engine_id (str):
            Output only. ID of the ad in the external engine account.
            This field is for Search Ads 360 account only, for example,
            Yahoo Japan, Microsoft, Baidu etc. For non-Search Ads 360
            entity, use "ad_group_ad.ad.id" instead.
        engine_status (google.ads.searchads360.v0.enums.types.AdGroupAdEngineStatusEnum.AdGroupAdEngineStatus):
            Output only. Additional status of the ad in
            the external engine account. Possible statuses
            (depending on the type of external account)
            include active, eligible, pending review, etc.
        last_modified_time (str):
            Output only. The datetime when this ad group
            ad was last modified. The datetime is in the
            customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    status: ad_group_ad_status.AdGroupAdStatusEnum.AdGroupAdStatus = proto.Field(
        proto.ENUM,
        number=3,
        enum=ad_group_ad_status.AdGroupAdStatusEnum.AdGroupAdStatus,
    )
    ad: gasr_ad.Ad = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gasr_ad.Ad,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=14,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    engine_id: str = proto.Field(
        proto.STRING,
        number=11,
    )
    engine_status: ad_group_ad_engine_status.AdGroupAdEngineStatusEnum.AdGroupAdEngineStatus = proto.Field(
        proto.ENUM,
        number=15,
        enum=ad_group_ad_engine_status.AdGroupAdEngineStatusEnum.AdGroupAdEngineStatus,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=12,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
