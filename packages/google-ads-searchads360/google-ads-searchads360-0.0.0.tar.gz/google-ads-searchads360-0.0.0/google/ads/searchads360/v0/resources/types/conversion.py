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

from google.ads.searchads360.v0.enums.types import asset_field_type as gase_asset_field_type
from google.ads.searchads360.v0.enums.types import attribution_type as gase_attribution_type
from google.ads.searchads360.v0.enums.types import conversion_status
from google.ads.searchads360.v0.enums.types import product_channel as gase_product_channel


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Conversion',
    },
)


class Conversion(proto.Message):
    r"""A conversion.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Output only. The resource name of the conversion. Conversion
            resource names have the form:

            ``customers/{customer_id}/conversions/{ad_group_id}~{criterion_id}~{ds_conversion_id}``
        id (int):
            Output only. The ID of the conversion

            This field is a member of `oneof`_ ``_id``.
        criterion_id (int):
            Output only. Search Ads 360 criterion ID. A
            value of 0 indicates that the criterion is
            unattributed.

            This field is a member of `oneof`_ ``_criterion_id``.
        merchant_id (int):
            Output only. The Search Ads 360 inventory
            account ID containing the product that was
            clicked on. Search Ads 360 generates this ID
            when you link an inventory account in Search Ads
            360.

            This field is a member of `oneof`_ ``_merchant_id``.
        ad_id (int):
            Output only. Ad ID. A value of 0 indicates
            that the ad is unattributed.

            This field is a member of `oneof`_ ``_ad_id``.
        click_id (str):
            Output only. A unique string, for the visit
            that the conversion is attributed to, that is
            passed to the landing page as the click id URL
            parameter.

            This field is a member of `oneof`_ ``_click_id``.
        visit_id (int):
            Output only. The Search Ads 360 visit ID that
            the conversion is attributed to.

            This field is a member of `oneof`_ ``_visit_id``.
        advertiser_conversion_id (str):
            Output only. For offline conversions, this is an ID provided
            by advertisers. If an advertiser doesn't specify such an ID,
            Search Ads 360 generates one. For online conversions, this
            is equal to the id column or the floodlight_order_id column
            depending on the advertiser's Floodlight instructions.

            This field is a member of `oneof`_ ``_advertiser_conversion_id``.
        product_id (str):
            Output only. The ID of the product clicked
            on.

            This field is a member of `oneof`_ ``_product_id``.
        product_channel (google.ads.searchads360.v0.enums.types.ProductChannelEnum.ProductChannel):
            Output only. The sales channel of the product
            that was clicked on: Online or Local.

            This field is a member of `oneof`_ ``_product_channel``.
        product_language_code (str):
            Output only. The language (ISO-639-1) that
            has been set for the Merchant Center feed
            containing data about the product.

            This field is a member of `oneof`_ ``_product_language_code``.
        product_store_id (str):
            Output only. The store in the Local Inventory
            Ad that was clicked on. This should match the
            store IDs used in your local products feed.

            This field is a member of `oneof`_ ``_product_store_id``.
        product_country_code (str):
            Output only. The country (ISO-3166-format)
            registered for the inventory feed that contains
            the product clicked on.

            This field is a member of `oneof`_ ``_product_country_code``.
        attribution_type (google.ads.searchads360.v0.enums.types.AttributionTypeEnum.AttributionType):
            Output only. What the conversion is
            attributed to: Visit or Keyword+Ad.

            This field is a member of `oneof`_ ``_attribution_type``.
        conversion_date_time (str):
            Output only. The timestamp of the conversion
            event.

            This field is a member of `oneof`_ ``_conversion_date_time``.
        conversion_last_modified_date_time (str):
            Output only. The timestamp of the last time
            the conversion was modified.

            This field is a member of `oneof`_ ``_conversion_last_modified_date_time``.
        conversion_visit_date_time (str):
            Output only. The timestamp of the visit that
            the conversion is attributed to.

            This field is a member of `oneof`_ ``_conversion_visit_date_time``.
        conversion_quantity (int):
            Output only. The quantity of items recorded
            by the conversion, as determined by the qty url
            parameter. The advertiser is responsible for
            dynamically populating the parameter (such as
            number of items sold in the conversion),
            otherwise it defaults to 1.

            This field is a member of `oneof`_ ``_conversion_quantity``.
        conversion_revenue_micros (int):
            Output only. The adjusted revenue in micros
            for the conversion event. This will always be in
            the currency of the serving account.

            This field is a member of `oneof`_ ``_conversion_revenue_micros``.
        floodlight_original_revenue (int):
            Output only. The original, unchanged revenue
            associated with the Floodlight event (in the
            currency of the current report), before
            Floodlight currency instruction modifications.

            This field is a member of `oneof`_ ``_floodlight_original_revenue``.
        floodlight_order_id (str):
            Output only. The Floodlight order ID provided
            by the advertiser for the conversion.

            This field is a member of `oneof`_ ``_floodlight_order_id``.
        status (google.ads.searchads360.v0.enums.types.ConversionStatusEnum.ConversionStatus):
            Output only. The status of the conversion,
            either ENABLED or REMOVED..

            This field is a member of `oneof`_ ``_status``.
        asset_id (int):
            Output only. ID of the asset which was
            interacted with during the conversion event.

            This field is a member of `oneof`_ ``_asset_id``.
        asset_field_type (google.ads.searchads360.v0.enums.types.AssetFieldTypeEnum.AssetFieldType):
            Output only. Asset field type of the
            conversion event.

            This field is a member of `oneof`_ ``_asset_field_type``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )
    criterion_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    merchant_id: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    ad_id: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    click_id: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    visit_id: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )
    advertiser_conversion_id: str = proto.Field(
        proto.STRING,
        number=8,
        optional=True,
    )
    product_id: str = proto.Field(
        proto.STRING,
        number=9,
        optional=True,
    )
    product_channel: gase_product_channel.ProductChannelEnum.ProductChannel = proto.Field(
        proto.ENUM,
        number=10,
        optional=True,
        enum=gase_product_channel.ProductChannelEnum.ProductChannel,
    )
    product_language_code: str = proto.Field(
        proto.STRING,
        number=11,
        optional=True,
    )
    product_store_id: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )
    product_country_code: str = proto.Field(
        proto.STRING,
        number=13,
        optional=True,
    )
    attribution_type: gase_attribution_type.AttributionTypeEnum.AttributionType = proto.Field(
        proto.ENUM,
        number=14,
        optional=True,
        enum=gase_attribution_type.AttributionTypeEnum.AttributionType,
    )
    conversion_date_time: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )
    conversion_last_modified_date_time: str = proto.Field(
        proto.STRING,
        number=16,
        optional=True,
    )
    conversion_visit_date_time: str = proto.Field(
        proto.STRING,
        number=17,
        optional=True,
    )
    conversion_quantity: int = proto.Field(
        proto.INT64,
        number=18,
        optional=True,
    )
    conversion_revenue_micros: int = proto.Field(
        proto.INT64,
        number=19,
        optional=True,
    )
    floodlight_original_revenue: int = proto.Field(
        proto.INT64,
        number=20,
        optional=True,
    )
    floodlight_order_id: str = proto.Field(
        proto.STRING,
        number=21,
        optional=True,
    )
    status: conversion_status.ConversionStatusEnum.ConversionStatus = proto.Field(
        proto.ENUM,
        number=22,
        optional=True,
        enum=conversion_status.ConversionStatusEnum.ConversionStatus,
    )
    asset_id: int = proto.Field(
        proto.INT64,
        number=23,
        optional=True,
    )
    asset_field_type: gase_asset_field_type.AssetFieldTypeEnum.AssetFieldType = proto.Field(
        proto.ENUM,
        number=24,
        optional=True,
        enum=gase_asset_field_type.AssetFieldTypeEnum.AssetFieldType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
