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

from google.ads.searchads360.v0.common.types import criteria
from google.ads.searchads360.v0.enums.types import campaign_criterion_status
from google.ads.searchads360.v0.enums.types import criterion_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'CampaignCriterion',
    },
)


class CampaignCriterion(proto.Message):
    r"""A campaign criterion.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign criterion.
            Campaign criterion resource names have the form:

            ``customers/{customer_id}/campaignCriteria/{campaign_id}~{criterion_id}``
        criterion_id (int):
            Output only. The ID of the criterion.

            This field is ignored during mutate.

            This field is a member of `oneof`_ ``_criterion_id``.
        display_name (str):
            Output only. The display name of the
            criterion.
            This field is ignored for mutates.
        bid_modifier (float):
            The modifier for the bids when the criterion
            matches. The modifier must be in the range: 0.1
            - 10.0. Most targetable criteria types support
            modifiers. Use 0 to opt out of a Device type.

            This field is a member of `oneof`_ ``_bid_modifier``.
        negative (bool):
            Immutable. Whether to target (``false``) or exclude
            (``true``) the criterion.

            This field is a member of `oneof`_ ``_negative``.
        type_ (google.ads.searchads360.v0.enums.types.CriterionTypeEnum.CriterionType):
            Output only. The type of the criterion.
        status (google.ads.searchads360.v0.enums.types.CampaignCriterionStatusEnum.CampaignCriterionStatus):
            The status of the criterion.
        last_modified_time (str):
            Output only. The datetime when this campaign
            criterion was last modified. The datetime is in
            the customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
        keyword (google.ads.searchads360.v0.common.types.KeywordInfo):
            Immutable. Keyword.

            This field is a member of `oneof`_ ``criterion``.
        location (google.ads.searchads360.v0.common.types.LocationInfo):
            Immutable. Location.

            This field is a member of `oneof`_ ``criterion``.
        device (google.ads.searchads360.v0.common.types.DeviceInfo):
            Immutable. Device.

            This field is a member of `oneof`_ ``criterion``.
        age_range (google.ads.searchads360.v0.common.types.AgeRangeInfo):
            Immutable. Age range.

            This field is a member of `oneof`_ ``criterion``.
        gender (google.ads.searchads360.v0.common.types.GenderInfo):
            Immutable. Gender.

            This field is a member of `oneof`_ ``criterion``.
        user_list (google.ads.searchads360.v0.common.types.UserListInfo):
            Immutable. User List.

            This field is a member of `oneof`_ ``criterion``.
        language (google.ads.searchads360.v0.common.types.LanguageInfo):
            Immutable. Language.

            This field is a member of `oneof`_ ``criterion``.
        webpage (google.ads.searchads360.v0.common.types.WebpageInfo):
            Immutable. Webpage.

            This field is a member of `oneof`_ ``criterion``.
        location_group (google.ads.searchads360.v0.common.types.LocationGroupInfo):
            Immutable. Location Group

            This field is a member of `oneof`_ ``criterion``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    criterion_id: int = proto.Field(
        proto.INT64,
        number=38,
        optional=True,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=43,
    )
    bid_modifier: float = proto.Field(
        proto.FLOAT,
        number=39,
        optional=True,
    )
    negative: bool = proto.Field(
        proto.BOOL,
        number=40,
        optional=True,
    )
    type_: criterion_type.CriterionTypeEnum.CriterionType = proto.Field(
        proto.ENUM,
        number=6,
        enum=criterion_type.CriterionTypeEnum.CriterionType,
    )
    status: campaign_criterion_status.CampaignCriterionStatusEnum.CampaignCriterionStatus = proto.Field(
        proto.ENUM,
        number=35,
        enum=campaign_criterion_status.CampaignCriterionStatusEnum.CampaignCriterionStatus,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=44,
    )
    keyword: criteria.KeywordInfo = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof='criterion',
        message=criteria.KeywordInfo,
    )
    location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof='criterion',
        message=criteria.LocationInfo,
    )
    device: criteria.DeviceInfo = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof='criterion',
        message=criteria.DeviceInfo,
    )
    age_range: criteria.AgeRangeInfo = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof='criterion',
        message=criteria.AgeRangeInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof='criterion',
        message=criteria.GenderInfo,
    )
    user_list: criteria.UserListInfo = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof='criterion',
        message=criteria.UserListInfo,
    )
    language: criteria.LanguageInfo = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof='criterion',
        message=criteria.LanguageInfo,
    )
    webpage: criteria.WebpageInfo = proto.Field(
        proto.MESSAGE,
        number=31,
        oneof='criterion',
        message=criteria.WebpageInfo,
    )
    location_group: criteria.LocationGroupInfo = proto.Field(
        proto.MESSAGE,
        number=34,
        oneof='criterion',
        message=criteria.LocationGroupInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
