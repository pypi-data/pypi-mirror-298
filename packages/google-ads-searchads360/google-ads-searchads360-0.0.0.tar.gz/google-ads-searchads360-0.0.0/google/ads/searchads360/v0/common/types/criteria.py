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

from google.ads.searchads360.v0.enums.types import age_range_type
from google.ads.searchads360.v0.enums.types import day_of_week as gase_day_of_week
from google.ads.searchads360.v0.enums.types import device
from google.ads.searchads360.v0.enums.types import gender_type
from google.ads.searchads360.v0.enums.types import keyword_match_type
from google.ads.searchads360.v0.enums.types import listing_group_type
from google.ads.searchads360.v0.enums.types import location_group_radius_units
from google.ads.searchads360.v0.enums.types import minute_of_hour
from google.ads.searchads360.v0.enums.types import webpage_condition_operand
from google.ads.searchads360.v0.enums.types import webpage_condition_operator


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'KeywordInfo',
        'LocationInfo',
        'DeviceInfo',
        'ListingGroupInfo',
        'AdScheduleInfo',
        'AgeRangeInfo',
        'GenderInfo',
        'UserListInfo',
        'LanguageInfo',
        'WebpageInfo',
        'WebpageConditionInfo',
        'LocationGroupInfo',
        'AudienceInfo',
    },
)


class KeywordInfo(proto.Message):
    r"""A keyword criterion.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            The text of the keyword (at most 80
            characters and 10 words).

            This field is a member of `oneof`_ ``_text``.
        match_type (google.ads.searchads360.v0.enums.types.KeywordMatchTypeEnum.KeywordMatchType):
            The match type of the keyword.
    """

    text: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    match_type: keyword_match_type.KeywordMatchTypeEnum.KeywordMatchType = proto.Field(
        proto.ENUM,
        number=2,
        enum=keyword_match_type.KeywordMatchTypeEnum.KeywordMatchType,
    )


class LocationInfo(proto.Message):
    r"""A location criterion.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        geo_target_constant (str):
            The geo target constant resource name.

            This field is a member of `oneof`_ ``_geo_target_constant``.
    """

    geo_target_constant: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class DeviceInfo(proto.Message):
    r"""A device criterion.
    Attributes:
        type_ (google.ads.searchads360.v0.enums.types.DeviceEnum.Device):
            Type of the device.
    """

    type_: device.DeviceEnum.Device = proto.Field(
        proto.ENUM,
        number=1,
        enum=device.DeviceEnum.Device,
    )


class ListingGroupInfo(proto.Message):
    r"""A listing group criterion.
    Attributes:
        type_ (google.ads.searchads360.v0.enums.types.ListingGroupTypeEnum.ListingGroupType):
            Type of the listing group.
    """

    type_: listing_group_type.ListingGroupTypeEnum.ListingGroupType = proto.Field(
        proto.ENUM,
        number=1,
        enum=listing_group_type.ListingGroupTypeEnum.ListingGroupType,
    )


class AdScheduleInfo(proto.Message):
    r"""Represents an AdSchedule criterion.

    AdSchedule is specified as the day of the week and a time
    interval within which ads will be shown.

    No more than six AdSchedules can be added for the same day.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        start_minute (google.ads.searchads360.v0.enums.types.MinuteOfHourEnum.MinuteOfHour):
            Minutes after the start hour at which this
            schedule starts.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        end_minute (google.ads.searchads360.v0.enums.types.MinuteOfHourEnum.MinuteOfHour):
            Minutes after the end hour at which this
            schedule ends. The schedule is exclusive of the
            end minute.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        start_hour (int):
            Starting hour in 24 hour time.
            This field must be between 0 and 23, inclusive.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.

            This field is a member of `oneof`_ ``_start_hour``.
        end_hour (int):
            Ending hour in 24 hour time; 24 signifies end
            of the day. This field must be between 0 and 24,
            inclusive.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.

            This field is a member of `oneof`_ ``_end_hour``.
        day_of_week (google.ads.searchads360.v0.enums.types.DayOfWeekEnum.DayOfWeek):
            Day of the week the schedule applies to.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
    """

    start_minute: minute_of_hour.MinuteOfHourEnum.MinuteOfHour = proto.Field(
        proto.ENUM,
        number=1,
        enum=minute_of_hour.MinuteOfHourEnum.MinuteOfHour,
    )
    end_minute: minute_of_hour.MinuteOfHourEnum.MinuteOfHour = proto.Field(
        proto.ENUM,
        number=2,
        enum=minute_of_hour.MinuteOfHourEnum.MinuteOfHour,
    )
    start_hour: int = proto.Field(
        proto.INT32,
        number=6,
        optional=True,
    )
    end_hour: int = proto.Field(
        proto.INT32,
        number=7,
        optional=True,
    )
    day_of_week: gase_day_of_week.DayOfWeekEnum.DayOfWeek = proto.Field(
        proto.ENUM,
        number=5,
        enum=gase_day_of_week.DayOfWeekEnum.DayOfWeek,
    )


class AgeRangeInfo(proto.Message):
    r"""An age range criterion.
    Attributes:
        type_ (google.ads.searchads360.v0.enums.types.AgeRangeTypeEnum.AgeRangeType):
            Type of the age range.
    """

    type_: age_range_type.AgeRangeTypeEnum.AgeRangeType = proto.Field(
        proto.ENUM,
        number=1,
        enum=age_range_type.AgeRangeTypeEnum.AgeRangeType,
    )


class GenderInfo(proto.Message):
    r"""A gender criterion.
    Attributes:
        type_ (google.ads.searchads360.v0.enums.types.GenderTypeEnum.GenderType):
            Type of the gender.
    """

    type_: gender_type.GenderTypeEnum.GenderType = proto.Field(
        proto.ENUM,
        number=1,
        enum=gender_type.GenderTypeEnum.GenderType,
    )


class UserListInfo(proto.Message):
    r"""A User List criterion. Represents a user list that is defined
    by the advertiser to be targeted.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        user_list (str):
            The User List resource name.

            This field is a member of `oneof`_ ``_user_list``.
    """

    user_list: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class LanguageInfo(proto.Message):
    r"""A language criterion.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        language_constant (str):
            The language constant resource name.

            This field is a member of `oneof`_ ``_language_constant``.
    """

    language_constant: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class WebpageInfo(proto.Message):
    r"""Represents a criterion for targeting webpages of an
    advertiser's website.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        criterion_name (str):
            The name of the criterion that is defined by
            this parameter. The name value will be used for
            identifying, sorting and filtering criteria with
            this type of parameters.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.

            This field is a member of `oneof`_ ``_criterion_name``.
        conditions (MutableSequence[google.ads.searchads360.v0.common.types.WebpageConditionInfo]):
            Conditions, or logical expressions, for
            webpage targeting. The list of webpage targeting
            conditions are and-ed together when evaluated
            for targeting. An empty list of conditions
            indicates all pages of the campaign's website
            are targeted.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        coverage_percentage (float):
            Website criteria coverage percentage. This is
            the computed percentage of website coverage
            based on the website target, negative website
            target and negative keywords in the ad group and
            campaign. For instance, when coverage returns as
            1, it indicates it has 100% coverage. This field
            is read-only.
    """

    criterion_name: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    conditions: MutableSequence['WebpageConditionInfo'] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message='WebpageConditionInfo',
    )
    coverage_percentage: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )


class WebpageConditionInfo(proto.Message):
    r"""Logical expression for targeting webpages of an advertiser's
    website.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        operand (google.ads.searchads360.v0.enums.types.WebpageConditionOperandEnum.WebpageConditionOperand):
            Operand of webpage targeting condition.
        operator (google.ads.searchads360.v0.enums.types.WebpageConditionOperatorEnum.WebpageConditionOperator):
            Operator of webpage targeting condition.
        argument (str):
            Argument of webpage targeting condition.

            This field is a member of `oneof`_ ``_argument``.
    """

    operand: webpage_condition_operand.WebpageConditionOperandEnum.WebpageConditionOperand = proto.Field(
        proto.ENUM,
        number=1,
        enum=webpage_condition_operand.WebpageConditionOperandEnum.WebpageConditionOperand,
    )
    operator: webpage_condition_operator.WebpageConditionOperatorEnum.WebpageConditionOperator = proto.Field(
        proto.ENUM,
        number=2,
        enum=webpage_condition_operator.WebpageConditionOperatorEnum.WebpageConditionOperator,
    )
    argument: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


class LocationGroupInfo(proto.Message):
    r"""A radius around a list of locations specified through a feed.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        geo_target_constants (MutableSequence[str]):
            Geo target constant(s) restricting the scope
            of the geographic area within the feed.
            Currently only one geo target constant is
            allowed.
        radius (int):
            Distance in units specifying the radius
            around targeted locations. This is required and
            must be set in CREATE operations.

            This field is a member of `oneof`_ ``_radius``.
        radius_units (google.ads.searchads360.v0.enums.types.LocationGroupRadiusUnitsEnum.LocationGroupRadiusUnits):
            Unit of the radius. Miles and meters are
            supported for geo target constants. Milli miles
            and meters are supported for feed item sets.
            This is required and must be set in CREATE
            operations.
        feed_item_sets (MutableSequence[str]):
            FeedItemSets whose FeedItems are targeted. If multiple IDs
            are specified, then all items that appear in at least one
            set are targeted. This field cannot be used with
            geo_target_constants. This is optional and can only be set
            in CREATE operations.
    """

    geo_target_constants: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    radius: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )
    radius_units: location_group_radius_units.LocationGroupRadiusUnitsEnum.LocationGroupRadiusUnits = proto.Field(
        proto.ENUM,
        number=4,
        enum=location_group_radius_units.LocationGroupRadiusUnitsEnum.LocationGroupRadiusUnits,
    )
    feed_item_sets: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )


class AudienceInfo(proto.Message):
    r"""An audience criterion.
    Attributes:
        audience (str):
            The Audience resource name.
    """

    audience: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
