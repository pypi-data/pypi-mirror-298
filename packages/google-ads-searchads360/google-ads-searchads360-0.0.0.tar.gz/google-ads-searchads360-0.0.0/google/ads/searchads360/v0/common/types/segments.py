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
from google.ads.searchads360.v0.common.types import value
from google.ads.searchads360.v0.enums.types import ad_network_type as gase_ad_network_type
from google.ads.searchads360.v0.enums.types import conversion_action_category as gase_conversion_action_category
from google.ads.searchads360.v0.enums.types import day_of_week as gase_day_of_week
from google.ads.searchads360.v0.enums.types import device as gase_device
from google.ads.searchads360.v0.enums.types import product_channel as gase_product_channel
from google.ads.searchads360.v0.enums.types import product_channel_exclusivity as gase_product_channel_exclusivity
from google.ads.searchads360.v0.enums.types import product_condition as gase_product_condition


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Segments',
        'Keyword',
        'AssetInteractionTarget',
    },
)


class Segments(proto.Message):
    r"""Segment only fields.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        ad_network_type (google.ads.searchads360.v0.enums.types.AdNetworkTypeEnum.AdNetworkType):
            Ad network type.
        conversion_action (str):
            Resource name of the conversion action.

            This field is a member of `oneof`_ ``_conversion_action``.
        conversion_action_category (google.ads.searchads360.v0.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            Conversion action category.
        conversion_action_name (str):
            Conversion action name.

            This field is a member of `oneof`_ ``_conversion_action_name``.
        conversion_custom_dimensions (MutableSequence[google.ads.searchads360.v0.common.types.Value]):
            The conversion custom dimensions.
        date (str):
            Date to which metrics apply.
            yyyy-MM-dd format, for example, 2018-04-17.

            This field is a member of `oneof`_ ``_date``.
        day_of_week (google.ads.searchads360.v0.enums.types.DayOfWeekEnum.DayOfWeek):
            Day of the week, for example, MONDAY.
        device (google.ads.searchads360.v0.enums.types.DeviceEnum.Device):
            Device to which metrics apply.
        geo_target_city (str):
            Resource name of the geo target constant that
            represents a city.

            This field is a member of `oneof`_ ``_geo_target_city``.
        geo_target_country (str):
            Resource name of the geo target constant that
            represents a country.

            This field is a member of `oneof`_ ``_geo_target_country``.
        geo_target_metro (str):
            Resource name of the geo target constant that
            represents a metro.

            This field is a member of `oneof`_ ``_geo_target_metro``.
        geo_target_region (str):
            Resource name of the geo target constant that
            represents a region.

            This field is a member of `oneof`_ ``_geo_target_region``.
        hour (int):
            Hour of day as a number between 0 and 23,
            inclusive.

            This field is a member of `oneof`_ ``_hour``.
        keyword (google.ads.searchads360.v0.common.types.Keyword):
            Keyword criterion.
        month (str):
            Month as represented by the date of the first
            day of a month. Formatted as yyyy-MM-dd.

            This field is a member of `oneof`_ ``_month``.
        product_bidding_category_level1 (str):
            Bidding category (level 1) of the product.

            This field is a member of `oneof`_ ``_product_bidding_category_level1``.
        product_bidding_category_level2 (str):
            Bidding category (level 2) of the product.

            This field is a member of `oneof`_ ``_product_bidding_category_level2``.
        product_bidding_category_level3 (str):
            Bidding category (level 3) of the product.

            This field is a member of `oneof`_ ``_product_bidding_category_level3``.
        product_bidding_category_level4 (str):
            Bidding category (level 4) of the product.

            This field is a member of `oneof`_ ``_product_bidding_category_level4``.
        product_bidding_category_level5 (str):
            Bidding category (level 5) of the product.

            This field is a member of `oneof`_ ``_product_bidding_category_level5``.
        product_brand (str):
            Brand of the product.

            This field is a member of `oneof`_ ``_product_brand``.
        product_channel (google.ads.searchads360.v0.enums.types.ProductChannelEnum.ProductChannel):
            Channel of the product.
        product_channel_exclusivity (google.ads.searchads360.v0.enums.types.ProductChannelExclusivityEnum.ProductChannelExclusivity):
            Channel exclusivity of the product.
        product_condition (google.ads.searchads360.v0.enums.types.ProductConditionEnum.ProductCondition):
            Condition of the product.
        product_country (str):
            Resource name of the geo target constant for
            the country of sale of the product.

            This field is a member of `oneof`_ ``_product_country``.
        product_custom_attribute0 (str):
            Custom attribute 0 of the product.

            This field is a member of `oneof`_ ``_product_custom_attribute0``.
        product_custom_attribute1 (str):
            Custom attribute 1 of the product.

            This field is a member of `oneof`_ ``_product_custom_attribute1``.
        product_custom_attribute2 (str):
            Custom attribute 2 of the product.

            This field is a member of `oneof`_ ``_product_custom_attribute2``.
        product_custom_attribute3 (str):
            Custom attribute 3 of the product.

            This field is a member of `oneof`_ ``_product_custom_attribute3``.
        product_custom_attribute4 (str):
            Custom attribute 4 of the product.

            This field is a member of `oneof`_ ``_product_custom_attribute4``.
        product_item_id (str):
            Item ID of the product.

            This field is a member of `oneof`_ ``_product_item_id``.
        product_language (str):
            Resource name of the language constant for
            the language of the product.

            This field is a member of `oneof`_ ``_product_language``.
        product_sold_bidding_category_level1 (str):
            Bidding category (level 1) of the product
            sold.

            This field is a member of `oneof`_ ``_product_sold_bidding_category_level1``.
        product_sold_bidding_category_level2 (str):
            Bidding category (level 2) of the product
            sold.

            This field is a member of `oneof`_ ``_product_sold_bidding_category_level2``.
        product_sold_bidding_category_level3 (str):
            Bidding category (level 3) of the product
            sold.

            This field is a member of `oneof`_ ``_product_sold_bidding_category_level3``.
        product_sold_bidding_category_level4 (str):
            Bidding category (level 4) of the product
            sold.

            This field is a member of `oneof`_ ``_product_sold_bidding_category_level4``.
        product_sold_bidding_category_level5 (str):
            Bidding category (level 5) of the product
            sold.

            This field is a member of `oneof`_ ``_product_sold_bidding_category_level5``.
        product_sold_brand (str):
            Brand of the product sold.

            This field is a member of `oneof`_ ``_product_sold_brand``.
        product_sold_condition (google.ads.searchads360.v0.enums.types.ProductConditionEnum.ProductCondition):
            Condition of the product sold.
        product_sold_custom_attribute0 (str):
            Custom attribute 0 of the product sold.

            This field is a member of `oneof`_ ``_product_sold_custom_attribute0``.
        product_sold_custom_attribute1 (str):
            Custom attribute 1 of the product sold.

            This field is a member of `oneof`_ ``_product_sold_custom_attribute1``.
        product_sold_custom_attribute2 (str):
            Custom attribute 2 of the product sold.

            This field is a member of `oneof`_ ``_product_sold_custom_attribute2``.
        product_sold_custom_attribute3 (str):
            Custom attribute 3 of the product sold.

            This field is a member of `oneof`_ ``_product_sold_custom_attribute3``.
        product_sold_custom_attribute4 (str):
            Custom attribute 4 of the product sold.

            This field is a member of `oneof`_ ``_product_sold_custom_attribute4``.
        product_sold_item_id (str):
            Item ID of the product sold.

            This field is a member of `oneof`_ ``_product_sold_item_id``.
        product_sold_title (str):
            Title of the product sold.

            This field is a member of `oneof`_ ``_product_sold_title``.
        product_sold_type_l1 (str):
            Type (level 1) of the product sold.

            This field is a member of `oneof`_ ``_product_sold_type_l1``.
        product_sold_type_l2 (str):
            Type (level 2) of the product sold.

            This field is a member of `oneof`_ ``_product_sold_type_l2``.
        product_sold_type_l3 (str):
            Type (level 3) of the product sold.

            This field is a member of `oneof`_ ``_product_sold_type_l3``.
        product_sold_type_l4 (str):
            Type (level 4) of the product sold.

            This field is a member of `oneof`_ ``_product_sold_type_l4``.
        product_sold_type_l5 (str):
            Type (level 5) of the product sold.

            This field is a member of `oneof`_ ``_product_sold_type_l5``.
        product_store_id (str):
            Store ID of the product.

            This field is a member of `oneof`_ ``_product_store_id``.
        product_title (str):
            Title of the product.

            This field is a member of `oneof`_ ``_product_title``.
        product_type_l1 (str):
            Type (level 1) of the product.

            This field is a member of `oneof`_ ``_product_type_l1``.
        product_type_l2 (str):
            Type (level 2) of the product.

            This field is a member of `oneof`_ ``_product_type_l2``.
        product_type_l3 (str):
            Type (level 3) of the product.

            This field is a member of `oneof`_ ``_product_type_l3``.
        product_type_l4 (str):
            Type (level 4) of the product.

            This field is a member of `oneof`_ ``_product_type_l4``.
        product_type_l5 (str):
            Type (level 5) of the product.

            This field is a member of `oneof`_ ``_product_type_l5``.
        quarter (str):
            Quarter as represented by the date of the
            first day of a quarter. Uses the calendar year
            for quarters, for example, the second quarter of
            2018 starts on 2018-04-01. Formatted as
            yyyy-MM-dd.

            This field is a member of `oneof`_ ``_quarter``.
        raw_event_conversion_dimensions (MutableSequence[google.ads.searchads360.v0.common.types.Value]):
            The raw event conversion dimensions.
        week (str):
            Week as defined as Monday through Sunday, and
            represented by the date of Monday. Formatted as
            yyyy-MM-dd.

            This field is a member of `oneof`_ ``_week``.
        year (int):
            Year, formatted as yyyy.

            This field is a member of `oneof`_ ``_year``.
        asset_interaction_target (google.ads.searchads360.v0.common.types.AssetInteractionTarget):
            Only used with CustomerAsset, CampaignAsset and AdGroupAsset
            metrics. Indicates whether the interaction metrics occurred
            on the asset itself or a different asset or ad unit.
            Interactions (for example, clicks) are counted across all
            the parts of the served ad (for example, Ad itself and other
            components like Sitelinks) when they are served together.
            When interaction_on_this_asset is true, it means the
            interactions are on this specific asset and when
            interaction_on_this_asset is false, it means the
            interactions is not on this specific asset but on other
            parts of the served ad this asset is served with.

            This field is a member of `oneof`_ ``_asset_interaction_target``.
    """

    ad_network_type: gase_ad_network_type.AdNetworkTypeEnum.AdNetworkType = proto.Field(
        proto.ENUM,
        number=3,
        enum=gase_ad_network_type.AdNetworkTypeEnum.AdNetworkType,
    )
    conversion_action: str = proto.Field(
        proto.STRING,
        number=146,
        optional=True,
    )
    conversion_action_category: gase_conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory = proto.Field(
        proto.ENUM,
        number=53,
        enum=gase_conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    conversion_action_name: str = proto.Field(
        proto.STRING,
        number=114,
        optional=True,
    )
    conversion_custom_dimensions: MutableSequence[value.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=188,
        message=value.Value,
    )
    date: str = proto.Field(
        proto.STRING,
        number=79,
        optional=True,
    )
    day_of_week: gase_day_of_week.DayOfWeekEnum.DayOfWeek = proto.Field(
        proto.ENUM,
        number=5,
        enum=gase_day_of_week.DayOfWeekEnum.DayOfWeek,
    )
    device: gase_device.DeviceEnum.Device = proto.Field(
        proto.ENUM,
        number=1,
        enum=gase_device.DeviceEnum.Device,
    )
    geo_target_city: str = proto.Field(
        proto.STRING,
        number=118,
        optional=True,
    )
    geo_target_country: str = proto.Field(
        proto.STRING,
        number=119,
        optional=True,
    )
    geo_target_metro: str = proto.Field(
        proto.STRING,
        number=122,
        optional=True,
    )
    geo_target_region: str = proto.Field(
        proto.STRING,
        number=126,
        optional=True,
    )
    hour: int = proto.Field(
        proto.INT32,
        number=88,
        optional=True,
    )
    keyword: 'Keyword' = proto.Field(
        proto.MESSAGE,
        number=61,
        message='Keyword',
    )
    month: str = proto.Field(
        proto.STRING,
        number=90,
        optional=True,
    )
    product_bidding_category_level1: str = proto.Field(
        proto.STRING,
        number=92,
        optional=True,
    )
    product_bidding_category_level2: str = proto.Field(
        proto.STRING,
        number=93,
        optional=True,
    )
    product_bidding_category_level3: str = proto.Field(
        proto.STRING,
        number=94,
        optional=True,
    )
    product_bidding_category_level4: str = proto.Field(
        proto.STRING,
        number=95,
        optional=True,
    )
    product_bidding_category_level5: str = proto.Field(
        proto.STRING,
        number=96,
        optional=True,
    )
    product_brand: str = proto.Field(
        proto.STRING,
        number=97,
        optional=True,
    )
    product_channel: gase_product_channel.ProductChannelEnum.ProductChannel = proto.Field(
        proto.ENUM,
        number=30,
        enum=gase_product_channel.ProductChannelEnum.ProductChannel,
    )
    product_channel_exclusivity: gase_product_channel_exclusivity.ProductChannelExclusivityEnum.ProductChannelExclusivity = proto.Field(
        proto.ENUM,
        number=31,
        enum=gase_product_channel_exclusivity.ProductChannelExclusivityEnum.ProductChannelExclusivity,
    )
    product_condition: gase_product_condition.ProductConditionEnum.ProductCondition = proto.Field(
        proto.ENUM,
        number=32,
        enum=gase_product_condition.ProductConditionEnum.ProductCondition,
    )
    product_country: str = proto.Field(
        proto.STRING,
        number=98,
        optional=True,
    )
    product_custom_attribute0: str = proto.Field(
        proto.STRING,
        number=99,
        optional=True,
    )
    product_custom_attribute1: str = proto.Field(
        proto.STRING,
        number=100,
        optional=True,
    )
    product_custom_attribute2: str = proto.Field(
        proto.STRING,
        number=101,
        optional=True,
    )
    product_custom_attribute3: str = proto.Field(
        proto.STRING,
        number=102,
        optional=True,
    )
    product_custom_attribute4: str = proto.Field(
        proto.STRING,
        number=103,
        optional=True,
    )
    product_item_id: str = proto.Field(
        proto.STRING,
        number=104,
        optional=True,
    )
    product_language: str = proto.Field(
        proto.STRING,
        number=105,
        optional=True,
    )
    product_sold_bidding_category_level1: str = proto.Field(
        proto.STRING,
        number=166,
        optional=True,
    )
    product_sold_bidding_category_level2: str = proto.Field(
        proto.STRING,
        number=167,
        optional=True,
    )
    product_sold_bidding_category_level3: str = proto.Field(
        proto.STRING,
        number=168,
        optional=True,
    )
    product_sold_bidding_category_level4: str = proto.Field(
        proto.STRING,
        number=169,
        optional=True,
    )
    product_sold_bidding_category_level5: str = proto.Field(
        proto.STRING,
        number=170,
        optional=True,
    )
    product_sold_brand: str = proto.Field(
        proto.STRING,
        number=171,
        optional=True,
    )
    product_sold_condition: gase_product_condition.ProductConditionEnum.ProductCondition = proto.Field(
        proto.ENUM,
        number=172,
        enum=gase_product_condition.ProductConditionEnum.ProductCondition,
    )
    product_sold_custom_attribute0: str = proto.Field(
        proto.STRING,
        number=173,
        optional=True,
    )
    product_sold_custom_attribute1: str = proto.Field(
        proto.STRING,
        number=174,
        optional=True,
    )
    product_sold_custom_attribute2: str = proto.Field(
        proto.STRING,
        number=175,
        optional=True,
    )
    product_sold_custom_attribute3: str = proto.Field(
        proto.STRING,
        number=176,
        optional=True,
    )
    product_sold_custom_attribute4: str = proto.Field(
        proto.STRING,
        number=177,
        optional=True,
    )
    product_sold_item_id: str = proto.Field(
        proto.STRING,
        number=178,
        optional=True,
    )
    product_sold_title: str = proto.Field(
        proto.STRING,
        number=179,
        optional=True,
    )
    product_sold_type_l1: str = proto.Field(
        proto.STRING,
        number=180,
        optional=True,
    )
    product_sold_type_l2: str = proto.Field(
        proto.STRING,
        number=181,
        optional=True,
    )
    product_sold_type_l3: str = proto.Field(
        proto.STRING,
        number=182,
        optional=True,
    )
    product_sold_type_l4: str = proto.Field(
        proto.STRING,
        number=183,
        optional=True,
    )
    product_sold_type_l5: str = proto.Field(
        proto.STRING,
        number=184,
        optional=True,
    )
    product_store_id: str = proto.Field(
        proto.STRING,
        number=106,
        optional=True,
    )
    product_title: str = proto.Field(
        proto.STRING,
        number=107,
        optional=True,
    )
    product_type_l1: str = proto.Field(
        proto.STRING,
        number=108,
        optional=True,
    )
    product_type_l2: str = proto.Field(
        proto.STRING,
        number=109,
        optional=True,
    )
    product_type_l3: str = proto.Field(
        proto.STRING,
        number=110,
        optional=True,
    )
    product_type_l4: str = proto.Field(
        proto.STRING,
        number=111,
        optional=True,
    )
    product_type_l5: str = proto.Field(
        proto.STRING,
        number=112,
        optional=True,
    )
    quarter: str = proto.Field(
        proto.STRING,
        number=128,
        optional=True,
    )
    raw_event_conversion_dimensions: MutableSequence[value.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=189,
        message=value.Value,
    )
    week: str = proto.Field(
        proto.STRING,
        number=130,
        optional=True,
    )
    year: int = proto.Field(
        proto.INT32,
        number=131,
        optional=True,
    )
    asset_interaction_target: 'AssetInteractionTarget' = proto.Field(
        proto.MESSAGE,
        number=139,
        optional=True,
        message='AssetInteractionTarget',
    )


class Keyword(proto.Message):
    r"""A Keyword criterion segment.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        ad_group_criterion (str):
            The AdGroupCriterion resource name.

            This field is a member of `oneof`_ ``_ad_group_criterion``.
        info (google.ads.searchads360.v0.common.types.KeywordInfo):
            Keyword info.
    """

    ad_group_criterion: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    info: criteria.KeywordInfo = proto.Field(
        proto.MESSAGE,
        number=2,
        message=criteria.KeywordInfo,
    )


class AssetInteractionTarget(proto.Message):
    r"""An AssetInteractionTarget segment.
    Attributes:
        asset (str):
            The asset resource name.
        interaction_on_this_asset (bool):
            Only used with CustomerAsset, CampaignAsset
            and AdGroupAsset metrics. Indicates whether the
            interaction metrics occurred on the asset itself
            or a different asset or ad unit.
    """

    asset: str = proto.Field(
        proto.STRING,
        number=1,
    )
    interaction_on_this_asset: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
