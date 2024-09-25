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

from google.ads.searchads360.v0.common.types import targeting_setting as gasc_targeting_setting
from google.ads.searchads360.v0.enums.types import ad_group_ad_rotation_mode
from google.ads.searchads360.v0.enums.types import ad_group_engine_status
from google.ads.searchads360.v0.enums.types import ad_group_status
from google.ads.searchads360.v0.enums.types import ad_group_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AdGroup',
    },
)


class AdGroup(proto.Message):
    r"""An ad group.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group. Ad group
            resource names have the form:

            ``customers/{customer_id}/adGroups/{ad_group_id}``
        id (int):
            Output only. The ID of the ad group.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            The name of the ad group.

            This field is required and should not be empty
            when creating new ad groups.

            It must contain fewer than 255 UTF-8 full-width
            characters.

            It must not contain any null (code point 0x0),
            NL line feed (code point 0xA) or carriage return
            (code point 0xD) characters.

            This field is a member of `oneof`_ ``_name``.
        status (google.ads.searchads360.v0.enums.types.AdGroupStatusEnum.AdGroupStatus):
            The status of the ad group.
        type_ (google.ads.searchads360.v0.enums.types.AdGroupTypeEnum.AdGroupType):
            Immutable. The type of the ad group.
        ad_rotation_mode (google.ads.searchads360.v0.enums.types.AdGroupAdRotationModeEnum.AdGroupAdRotationMode):
            The ad rotation mode of the ad group.
        cpc_bid_micros (int):
            The maximum CPC (cost-per-click) bid.

            This field is a member of `oneof`_ ``_cpc_bid_micros``.
        creation_time (str):
            Output only. The timestamp when this ad_group was created.
            The timestamp is in the customer's time zone and in
            "yyyy-MM-dd HH:mm:ss" format.
        engine_status (google.ads.searchads360.v0.enums.types.AdGroupEngineStatusEnum.AdGroupEngineStatus):
            Output only. The Engine Status for ad group.

            This field is a member of `oneof`_ ``_engine_status``.
        targeting_setting (google.ads.searchads360.v0.common.types.TargetingSetting):
            Setting for targeting related features.
        labels (MutableSequence[str]):
            Output only. The resource names of labels
            attached to this ad group.
        engine_id (str):
            Output only. ID of the ad group in the external engine
            account. This field is for non-Google Ads account only, for
            example, Yahoo Japan, Microsoft, Baidu etc. For Google Ads
            entity, use "ad_group.id" instead.
        start_date (str):
            Output only. Date when this ad group starts
            serving ads. By default, the ad group starts now
            or the ad group's start date, whichever is
            later. If this field is set, then the ad group
            starts at the beginning of the specified date in
            the customer's time zone. This field is only
            available for Microsoft Advertising and Facebook
            gateway accounts.

            Format: YYYY-MM-DD
            Example: 2019-03-14
        end_date (str):
            Output only. Date when the ad group ends
            serving ads. By default, the ad group ends on
            the ad group's end date. If this field is set,
            then the ad group ends at the end of the
            specified date in the customer's time zone. This
            field is only available for Microsoft
            Advertising and Facebook gateway accounts.

            Format: YYYY-MM-DD
            Example: 2019-03-14
        language_code (str):
            Output only. The language of the ads and
            keywords in an ad group. This field is only
            available for Microsoft Advertising accounts.
            More details:

            https://docs.microsoft.com/en-us/advertising/guides/ad-languages?view=bingads-13#adlanguage
        last_modified_time (str):
            Output only. The datetime when this ad group
            was last modified. The datetime is in the
            customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=34,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=35,
        optional=True,
    )
    status: ad_group_status.AdGroupStatusEnum.AdGroupStatus = proto.Field(
        proto.ENUM,
        number=5,
        enum=ad_group_status.AdGroupStatusEnum.AdGroupStatus,
    )
    type_: ad_group_type.AdGroupTypeEnum.AdGroupType = proto.Field(
        proto.ENUM,
        number=12,
        enum=ad_group_type.AdGroupTypeEnum.AdGroupType,
    )
    ad_rotation_mode: ad_group_ad_rotation_mode.AdGroupAdRotationModeEnum.AdGroupAdRotationMode = proto.Field(
        proto.ENUM,
        number=22,
        enum=ad_group_ad_rotation_mode.AdGroupAdRotationModeEnum.AdGroupAdRotationMode,
    )
    cpc_bid_micros: int = proto.Field(
        proto.INT64,
        number=39,
        optional=True,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=60,
    )
    engine_status: ad_group_engine_status.AdGroupEngineStatusEnum.AdGroupEngineStatus = proto.Field(
        proto.ENUM,
        number=61,
        optional=True,
        enum=ad_group_engine_status.AdGroupEngineStatusEnum.AdGroupEngineStatus,
    )
    targeting_setting: gasc_targeting_setting.TargetingSetting = proto.Field(
        proto.MESSAGE,
        number=25,
        message=gasc_targeting_setting.TargetingSetting,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=49,
    )
    engine_id: str = proto.Field(
        proto.STRING,
        number=50,
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=51,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=52,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=53,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=55,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
