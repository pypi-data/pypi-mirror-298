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

from google.ads.searchads360.v0.enums.types import account_status as gase_account_status
from google.ads.searchads360.v0.enums.types import account_type as gase_account_type
from google.ads.searchads360.v0.enums.types import conversion_tracking_status_enum
from google.ads.searchads360.v0.enums.types import customer_status


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Customer',
        'ConversionTrackingSetting',
        'DoubleClickCampaignManagerSetting',
    },
)


class Customer(proto.Message):
    r"""A customer.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer. Customer
            resource names have the form:

            ``customers/{customer_id}``
        id (int):
            Output only. The ID of the customer.

            This field is a member of `oneof`_ ``_id``.
        descriptive_name (str):
            Optional, non-unique descriptive name of the
            customer.

            This field is a member of `oneof`_ ``_descriptive_name``.
        currency_code (str):
            Immutable. The currency in which the account
            operates. A subset of the currency codes from
            the ISO 4217 standard is supported.

            This field is a member of `oneof`_ ``_currency_code``.
        time_zone (str):
            Immutable. The local timezone ID of the
            customer.

            This field is a member of `oneof`_ ``_time_zone``.
        tracking_url_template (str):
            The URL template for constructing a tracking
            URL out of parameters.

            This field is a member of `oneof`_ ``_tracking_url_template``.
        final_url_suffix (str):
            The URL template for appending params to the
            final URL.

            This field is a member of `oneof`_ ``_final_url_suffix``.
        auto_tagging_enabled (bool):
            Whether auto-tagging is enabled for the
            customer.

            This field is a member of `oneof`_ ``_auto_tagging_enabled``.
        manager (bool):
            Output only. Whether the customer is a
            manager.

            This field is a member of `oneof`_ ``_manager``.
        conversion_tracking_setting (google.ads.searchads360.v0.resources.types.ConversionTrackingSetting):
            Output only. Conversion tracking setting for
            a customer.
        account_type (google.ads.searchads360.v0.enums.types.AccountTypeEnum.AccountType):
            Output only. Engine account type, for
            example, Google Ads, Microsoft Advertising,
            Yahoo Japan, Baidu, Facebook, Engine Track, etc.
        double_click_campaign_manager_setting (google.ads.searchads360.v0.resources.types.DoubleClickCampaignManagerSetting):
            Output only. DoubleClick Campaign Manager
            (DCM) setting for a manager customer.
        account_status (google.ads.searchads360.v0.enums.types.AccountStatusEnum.AccountStatus):
            Output only. Account status, for example,
            Enabled, Paused, Removed, etc.
        last_modified_time (str):
            Output only. The datetime when this customer
            was last modified. The datetime is in the
            customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
        engine_id (str):
            Output only. ID of the account in the
            external engine account.
        status (google.ads.searchads360.v0.enums.types.CustomerStatusEnum.CustomerStatus):
            Output only. The status of the customer.
        creation_time (str):
            Output only. The timestamp when this customer
            was created. The timestamp is in the customer's
            time zone and in "yyyy-MM-dd HH:mm:ss" format.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=19,
        optional=True,
    )
    descriptive_name: str = proto.Field(
        proto.STRING,
        number=20,
        optional=True,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=21,
        optional=True,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=22,
        optional=True,
    )
    tracking_url_template: str = proto.Field(
        proto.STRING,
        number=23,
        optional=True,
    )
    final_url_suffix: str = proto.Field(
        proto.STRING,
        number=24,
        optional=True,
    )
    auto_tagging_enabled: bool = proto.Field(
        proto.BOOL,
        number=25,
        optional=True,
    )
    manager: bool = proto.Field(
        proto.BOOL,
        number=27,
        optional=True,
    )
    conversion_tracking_setting: 'ConversionTrackingSetting' = proto.Field(
        proto.MESSAGE,
        number=14,
        message='ConversionTrackingSetting',
    )
    account_type: gase_account_type.AccountTypeEnum.AccountType = proto.Field(
        proto.ENUM,
        number=31,
        enum=gase_account_type.AccountTypeEnum.AccountType,
    )
    double_click_campaign_manager_setting: 'DoubleClickCampaignManagerSetting' = proto.Field(
        proto.MESSAGE,
        number=32,
        message='DoubleClickCampaignManagerSetting',
    )
    account_status: gase_account_status.AccountStatusEnum.AccountStatus = proto.Field(
        proto.ENUM,
        number=33,
        enum=gase_account_status.AccountStatusEnum.AccountStatus,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=34,
    )
    engine_id: str = proto.Field(
        proto.STRING,
        number=35,
    )
    status: customer_status.CustomerStatusEnum.CustomerStatus = proto.Field(
        proto.ENUM,
        number=36,
        enum=customer_status.CustomerStatusEnum.CustomerStatus,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=42,
    )


class ConversionTrackingSetting(proto.Message):
    r"""A collection of customer-wide settings related to Search Ads
    360 Conversion Tracking.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        conversion_tracking_id (int):
            Output only. The conversion tracking id used for this
            account. This id doesn't indicate whether the customer uses
            conversion tracking (conversion_tracking_status does). This
            field is read-only.

            This field is a member of `oneof`_ ``_conversion_tracking_id``.
        google_ads_cross_account_conversion_tracking_id (int):
            Output only. The conversion tracking id of the customer's
            manager. This is set when the customer is opted into
            conversion tracking, and it overrides
            conversion_tracking_id. This field can only be managed
            through the Google Ads UI. This field is read-only.

            This field is a member of `oneof`_ ``_google_ads_cross_account_conversion_tracking_id``.
        cross_account_conversion_tracking_id (int):
            Output only. The conversion tracking id of the customer's
            manager. This is set when the customer is opted into
            cross-account conversion tracking, and it overrides
            conversion_tracking_id.

            This field is a member of `oneof`_ ``_cross_account_conversion_tracking_id``.
        accepted_customer_data_terms (bool):
            Output only. Whether the customer has
            accepted customer data terms. If using
            cross-account conversion tracking, this value is
            inherited from the manager. This field is
            read-only. For more
            information, see
            https://support.google.com/adspolicy/answer/7475709.
        conversion_tracking_status (google.ads.searchads360.v0.enums.types.ConversionTrackingStatusEnum.ConversionTrackingStatus):
            Output only. Conversion tracking status. It indicates
            whether the customer is using conversion tracking, and who
            is the conversion tracking owner of this customer. If this
            customer is using cross-account conversion tracking, the
            value returned will differ based on the
            ``login-customer-id`` of the request.
        enhanced_conversions_for_leads_enabled (bool):
            Output only. Whether the customer is opted-in
            for enhanced conversions for leads. If using
            cross-account conversion tracking, this value is
            inherited from the manager. This field is
            read-only.
        google_ads_conversion_customer (str):
            Output only. The resource name of the
            customer where conversions are created and
            managed. This field is read-only.
    """

    conversion_tracking_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    google_ads_cross_account_conversion_tracking_id: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    cross_account_conversion_tracking_id: int = proto.Field(
        proto.INT64,
        number=37,
        optional=True,
    )
    accepted_customer_data_terms: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    conversion_tracking_status: conversion_tracking_status_enum.ConversionTrackingStatusEnum.ConversionTrackingStatus = proto.Field(
        proto.ENUM,
        number=6,
        enum=conversion_tracking_status_enum.ConversionTrackingStatusEnum.ConversionTrackingStatus,
    )
    enhanced_conversions_for_leads_enabled: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    google_ads_conversion_customer: str = proto.Field(
        proto.STRING,
        number=8,
    )


class DoubleClickCampaignManagerSetting(proto.Message):
    r"""DoubleClick Campaign Manager (DCM) setting for a manager
    customer.

    Attributes:
        advertiser_id (int):
            Output only. ID of the Campaign Manager
            advertiser associated with this customer.
        network_id (int):
            Output only. ID of the Campaign Manager
            network associated with this customer.
        time_zone (str):
            Output only. Time zone of the Campaign Manager network
            associated with this customer in IANA Time Zone Database
            format, such as America/New_York.
    """

    advertiser_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    network_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
