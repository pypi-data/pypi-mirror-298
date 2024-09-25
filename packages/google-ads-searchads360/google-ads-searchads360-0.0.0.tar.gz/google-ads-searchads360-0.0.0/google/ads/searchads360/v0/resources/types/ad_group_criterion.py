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
from google.ads.searchads360.v0.enums.types import ad_group_criterion_engine_status
from google.ads.searchads360.v0.enums.types import ad_group_criterion_status
from google.ads.searchads360.v0.enums.types import criterion_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AdGroupCriterion',
    },
)


class AdGroupCriterion(proto.Message):
    r"""An ad group criterion. The ad_group_criterion report only returns
    criteria that were explicitly added to the ad group.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group criterion. Ad
            group criterion resource names have the form:

            ``customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}``
        criterion_id (int):
            Output only. The ID of the criterion.

            This field is a member of `oneof`_ ``_criterion_id``.
        creation_time (str):
            Output only. The timestamp when this ad group
            criterion was created. The timestamp is in the
            customer's time zone and in "yyyy-MM-dd
            HH:mm:ss" format.
        status (google.ads.searchads360.v0.enums.types.AdGroupCriterionStatusEnum.AdGroupCriterionStatus):
            The status of the criterion.

            This is the status of the ad group criterion
            entity, set by the client. Note: UI reports may
            incorporate additional information that affects
            whether a criterion is eligible to run. In some
            cases a criterion that's REMOVED in the API can
            still show as enabled in the UI. For example,
            campaigns by default show to users of all age
            ranges unless excluded. The UI will show each
            age range as "enabled", since they're eligible
            to see the ads; but AdGroupCriterion.status will
            show "removed", since no positive criterion was
            added.
        quality_info (google.ads.searchads360.v0.resources.types.AdGroupCriterion.QualityInfo):
            Output only. Information regarding the
            quality of the criterion.
        ad_group (str):
            Immutable. The ad group to which the
            criterion belongs.

            This field is a member of `oneof`_ ``_ad_group``.
        type_ (google.ads.searchads360.v0.enums.types.CriterionTypeEnum.CriterionType):
            Output only. The type of the criterion.
        negative (bool):
            Immutable. Whether to target (``false``) or exclude
            (``true``) the criterion.

            This field is immutable. To switch a criterion from positive
            to negative, remove then re-add it.

            This field is a member of `oneof`_ ``_negative``.
        labels (MutableSequence[str]):
            Output only. The resource names of labels
            attached to this ad group criterion.
        bid_modifier (float):
            The modifier for the bid when the criterion
            matches. The modifier must be in the range: 0.1
            - 10.0. Most targetable criteria types support
            modifiers.

            This field is a member of `oneof`_ ``_bid_modifier``.
        cpc_bid_micros (int):
            The CPC (cost-per-click) bid.

            This field is a member of `oneof`_ ``_cpc_bid_micros``.
        effective_cpc_bid_micros (int):
            Output only. The effective CPC
            (cost-per-click) bid.

            This field is a member of `oneof`_ ``_effective_cpc_bid_micros``.
        position_estimates (google.ads.searchads360.v0.resources.types.AdGroupCriterion.PositionEstimates):
            Output only. Estimates for criterion bids at
            various positions.
        final_urls (MutableSequence[str]):
            The list of possible final URLs after all
            cross-domain redirects for the ad.
        engine_status (google.ads.searchads360.v0.enums.types.AdGroupCriterionEngineStatusEnum.AdGroupCriterionEngineStatus):
            Output only. The Engine Status for ad group
            criterion.

            This field is a member of `oneof`_ ``_engine_status``.
        final_url_suffix (str):
            URL template for appending params to final
            URL.

            This field is a member of `oneof`_ ``_final_url_suffix``.
        tracking_url_template (str):
            The URL template for constructing a tracking
            URL.

            This field is a member of `oneof`_ ``_tracking_url_template``.
        engine_id (str):
            Output only. ID of the ad group criterion in the external
            engine account. This field is for non-Google Ads account
            only, for example, Yahoo Japan, Microsoft, Baidu etc. For
            Google Ads entity, use "ad_group_criterion.criterion_id"
            instead.
        last_modified_time (str):
            Output only. The datetime when this ad group
            criterion was last modified. The datetime is in
            the customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
        keyword (google.ads.searchads360.v0.common.types.KeywordInfo):
            Immutable. Keyword.

            This field is a member of `oneof`_ ``criterion``.
        listing_group (google.ads.searchads360.v0.common.types.ListingGroupInfo):
            Immutable. Listing group.

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
        webpage (google.ads.searchads360.v0.common.types.WebpageInfo):
            Immutable. Webpage

            This field is a member of `oneof`_ ``criterion``.
        location (google.ads.searchads360.v0.common.types.LocationInfo):
            Immutable. Location.

            This field is a member of `oneof`_ ``criterion``.
    """

    class QualityInfo(proto.Message):
        r"""A container for ad group criterion quality information.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            quality_score (int):
                Output only. The quality score.

                This field may not be populated if Google does
                not have enough information to determine a
                value.

                This field is a member of `oneof`_ ``_quality_score``.
        """

        quality_score: int = proto.Field(
            proto.INT32,
            number=5,
            optional=True,
        )

    class PositionEstimates(proto.Message):
        r"""Estimates for criterion bids at various positions.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            top_of_page_cpc_micros (int):
                Output only. The estimate of the CPC bid
                required for ad to be displayed at the top of
                the first page of search results.

                This field is a member of `oneof`_ ``_top_of_page_cpc_micros``.
        """

        top_of_page_cpc_micros: int = proto.Field(
            proto.INT64,
            number=8,
            optional=True,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    criterion_id: int = proto.Field(
        proto.INT64,
        number=56,
        optional=True,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=81,
    )
    status: ad_group_criterion_status.AdGroupCriterionStatusEnum.AdGroupCriterionStatus = proto.Field(
        proto.ENUM,
        number=3,
        enum=ad_group_criterion_status.AdGroupCriterionStatusEnum.AdGroupCriterionStatus,
    )
    quality_info: QualityInfo = proto.Field(
        proto.MESSAGE,
        number=4,
        message=QualityInfo,
    )
    ad_group: str = proto.Field(
        proto.STRING,
        number=57,
        optional=True,
    )
    type_: criterion_type.CriterionTypeEnum.CriterionType = proto.Field(
        proto.ENUM,
        number=25,
        enum=criterion_type.CriterionTypeEnum.CriterionType,
    )
    negative: bool = proto.Field(
        proto.BOOL,
        number=58,
        optional=True,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=60,
    )
    bid_modifier: float = proto.Field(
        proto.DOUBLE,
        number=61,
        optional=True,
    )
    cpc_bid_micros: int = proto.Field(
        proto.INT64,
        number=62,
        optional=True,
    )
    effective_cpc_bid_micros: int = proto.Field(
        proto.INT64,
        number=66,
        optional=True,
    )
    position_estimates: PositionEstimates = proto.Field(
        proto.MESSAGE,
        number=10,
        message=PositionEstimates,
    )
    final_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=70,
    )
    engine_status: ad_group_criterion_engine_status.AdGroupCriterionEngineStatusEnum.AdGroupCriterionEngineStatus = proto.Field(
        proto.ENUM,
        number=80,
        optional=True,
        enum=ad_group_criterion_engine_status.AdGroupCriterionEngineStatusEnum.AdGroupCriterionEngineStatus,
    )
    final_url_suffix: str = proto.Field(
        proto.STRING,
        number=72,
        optional=True,
    )
    tracking_url_template: str = proto.Field(
        proto.STRING,
        number=73,
        optional=True,
    )
    engine_id: str = proto.Field(
        proto.STRING,
        number=76,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=78,
    )
    keyword: criteria.KeywordInfo = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof='criterion',
        message=criteria.KeywordInfo,
    )
    listing_group: criteria.ListingGroupInfo = proto.Field(
        proto.MESSAGE,
        number=32,
        oneof='criterion',
        message=criteria.ListingGroupInfo,
    )
    age_range: criteria.AgeRangeInfo = proto.Field(
        proto.MESSAGE,
        number=36,
        oneof='criterion',
        message=criteria.AgeRangeInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE,
        number=37,
        oneof='criterion',
        message=criteria.GenderInfo,
    )
    user_list: criteria.UserListInfo = proto.Field(
        proto.MESSAGE,
        number=42,
        oneof='criterion',
        message=criteria.UserListInfo,
    )
    webpage: criteria.WebpageInfo = proto.Field(
        proto.MESSAGE,
        number=46,
        oneof='criterion',
        message=criteria.WebpageInfo,
    )
    location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE,
        number=82,
        oneof='criterion',
        message=criteria.LocationInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
