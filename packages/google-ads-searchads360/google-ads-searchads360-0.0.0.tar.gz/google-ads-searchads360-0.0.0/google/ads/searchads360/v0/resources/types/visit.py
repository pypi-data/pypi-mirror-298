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
from google.ads.searchads360.v0.enums.types import product_channel as gase_product_channel


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Visit',
    },
)


class Visit(proto.Message):
    r"""A visit.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Output only. The resource name of the visit. Visit resource
            names have the form:

            ``customers/{customer_id}/visits/{ad_group_id}~{criterion_id}~{ds_visit_id}``
        id (int):
            Output only. The ID of the visit.

            This field is a member of `oneof`_ ``_id``.
        criterion_id (int):
            Output only. Search Ads 360 keyword ID. A
            value of 0 indicates that the keyword is
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
            Output only. A unique string for each visit
            that is passed to the landing page as the click
            id URL parameter.

            This field is a member of `oneof`_ ``_click_id``.
        visit_date_time (str):
            Output only. The timestamp of the visit
            event. The timestamp is in the customer's time
            zone and in "yyyy-MM-dd HH:mm:ss" format.

            This field is a member of `oneof`_ ``_visit_date_time``.
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
            Output only. The country (ISO-3166 format)
            registered for the inventory feed that contains
            the product clicked on.

            This field is a member of `oneof`_ ``_product_country_code``.
        asset_id (int):
            Output only. ID of the asset which was
            interacted with during the visit event.

            This field is a member of `oneof`_ ``_asset_id``.
        asset_field_type (google.ads.searchads360.v0.enums.types.AssetFieldTypeEnum.AssetFieldType):
            Output only. Asset field type of the visit
            event.

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
    visit_date_time: str = proto.Field(
        proto.STRING,
        number=7,
        optional=True,
    )
    product_id: str = proto.Field(
        proto.STRING,
        number=8,
        optional=True,
    )
    product_channel: gase_product_channel.ProductChannelEnum.ProductChannel = proto.Field(
        proto.ENUM,
        number=9,
        optional=True,
        enum=gase_product_channel.ProductChannelEnum.ProductChannel,
    )
    product_language_code: str = proto.Field(
        proto.STRING,
        number=10,
        optional=True,
    )
    product_store_id: str = proto.Field(
        proto.STRING,
        number=11,
        optional=True,
    )
    product_country_code: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )
    asset_id: int = proto.Field(
        proto.INT64,
        number=13,
        optional=True,
    )
    asset_field_type: gase_asset_field_type.AssetFieldTypeEnum.AssetFieldType = proto.Field(
        proto.ENUM,
        number=14,
        optional=True,
        enum=gase_asset_field_type.AssetFieldTypeEnum.AssetFieldType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
