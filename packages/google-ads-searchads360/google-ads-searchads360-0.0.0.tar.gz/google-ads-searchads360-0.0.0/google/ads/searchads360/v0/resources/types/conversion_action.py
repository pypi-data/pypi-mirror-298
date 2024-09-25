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

from google.ads.searchads360.v0.enums.types import attribution_model as gase_attribution_model
from google.ads.searchads360.v0.enums.types import conversion_action_category
from google.ads.searchads360.v0.enums.types import conversion_action_status
from google.ads.searchads360.v0.enums.types import conversion_action_type
from google.ads.searchads360.v0.enums.types import data_driven_model_status as gase_data_driven_model_status


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'ConversionAction',
    },
)


class ConversionAction(proto.Message):
    r"""A conversion action.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the conversion action.
            Conversion action resource names have the form:

            ``customers/{customer_id}/conversionActions/{conversion_action_id}``
        id (int):
            Output only. The ID of the conversion action.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            The name of the conversion action.

            This field is required and should not be empty
            when creating new conversion actions.

            This field is a member of `oneof`_ ``_name``.
        creation_time (str):
            Output only. Timestamp of the Floodlight
            activity's creation, formatted in ISO 8601.
        status (google.ads.searchads360.v0.enums.types.ConversionActionStatusEnum.ConversionActionStatus):
            The status of this conversion action for
            conversion event accrual.
        type_ (google.ads.searchads360.v0.enums.types.ConversionActionTypeEnum.ConversionActionType):
            Immutable. The type of this conversion
            action.
        primary_for_goal (bool):
            If a conversion action's primary_for_goal bit is false, the
            conversion action is non-biddable for all campaigns
            regardless of their customer conversion goal or campaign
            conversion goal. However, custom conversion goals do not
            respect primary_for_goal, so if a campaign has a custom
            conversion goal configured with a primary_for_goal = false
            conversion action, that conversion action is still biddable.
            By default, primary_for_goal will be true if not set. In V9,
            primary_for_goal can only be set to false after creation
            through an 'update' operation because it's not declared as
            optional.

            This field is a member of `oneof`_ ``_primary_for_goal``.
        category (google.ads.searchads360.v0.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            The category of conversions reported for this
            conversion action.
        owner_customer (str):
            Output only. The resource name of the
            conversion action owner customer, or null if
            this is a system-defined conversion action.

            This field is a member of `oneof`_ ``_owner_customer``.
        include_in_client_account_conversions_metric (bool):
            Whether this conversion action should be included in the
            "client_account_conversions" metric.

            This field is a member of `oneof`_ ``_include_in_client_account_conversions_metric``.
        include_in_conversions_metric (bool):
            Output only. Whether this conversion action
            should be included in the "conversions" metric.

            This field is a member of `oneof`_ ``_include_in_conversions_metric``.
        click_through_lookback_window_days (int):
            The maximum number of days that may elapse
            between an interaction (for example, a click)
            and a conversion event.

            This field is a member of `oneof`_ ``_click_through_lookback_window_days``.
        value_settings (google.ads.searchads360.v0.resources.types.ConversionAction.ValueSettings):
            Settings related to the value for conversion
            events associated with this conversion action.
        attribution_model_settings (google.ads.searchads360.v0.resources.types.ConversionAction.AttributionModelSettings):
            Settings related to this conversion action's
            attribution model.
        app_id (str):
            App ID for an app conversion action.

            This field is a member of `oneof`_ ``_app_id``.
        floodlight_settings (google.ads.searchads360.v0.resources.types.ConversionAction.FloodlightSettings):
            Output only. Floodlight settings for
            Floodlight conversion types.
    """

    class AttributionModelSettings(proto.Message):
        r"""Settings related to this conversion action's attribution
        model.

        Attributes:
            attribution_model (google.ads.searchads360.v0.enums.types.AttributionModelEnum.AttributionModel):
                The attribution model type of this conversion
                action.
            data_driven_model_status (google.ads.searchads360.v0.enums.types.DataDrivenModelStatusEnum.DataDrivenModelStatus):
                Output only. The status of the data-driven
                attribution model for the conversion action.
        """

        attribution_model: gase_attribution_model.AttributionModelEnum.AttributionModel = proto.Field(
            proto.ENUM,
            number=1,
            enum=gase_attribution_model.AttributionModelEnum.AttributionModel,
        )
        data_driven_model_status: gase_data_driven_model_status.DataDrivenModelStatusEnum.DataDrivenModelStatus = proto.Field(
            proto.ENUM,
            number=2,
            enum=gase_data_driven_model_status.DataDrivenModelStatusEnum.DataDrivenModelStatus,
        )

    class ValueSettings(proto.Message):
        r"""Settings related to the value for conversion events
        associated with this conversion action.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            default_value (float):
                The value to use when conversion events for
                this conversion action are sent with an invalid,
                disallowed or missing value, or when this
                conversion action is configured to always use
                the default value.

                This field is a member of `oneof`_ ``_default_value``.
            default_currency_code (str):
                The currency code to use when conversion
                events for this conversion action are sent with
                an invalid or missing currency code, or when
                this conversion action is configured to always
                use the default value.

                This field is a member of `oneof`_ ``_default_currency_code``.
            always_use_default_value (bool):
                Controls whether the default value and
                default currency code are used in place of the
                value and currency code specified in conversion
                events for this conversion action.

                This field is a member of `oneof`_ ``_always_use_default_value``.
        """

        default_value: float = proto.Field(
            proto.DOUBLE,
            number=4,
            optional=True,
        )
        default_currency_code: str = proto.Field(
            proto.STRING,
            number=5,
            optional=True,
        )
        always_use_default_value: bool = proto.Field(
            proto.BOOL,
            number=6,
            optional=True,
        )

    class FloodlightSettings(proto.Message):
        r"""Settings related to a Floodlight conversion action.
        Attributes:
            activity_group_tag (str):
                Output only. String used to identify a
                Floodlight activity group when reporting
                conversions.
            activity_tag (str):
                Output only. String used to identify a
                Floodlight activity when reporting conversions.
            activity_id (int):
                Output only. ID of the Floodlight activity in
                DoubleClick Campaign Manager (DCM).
        """

        activity_group_tag: str = proto.Field(
            proto.STRING,
            number=1,
        )
        activity_tag: str = proto.Field(
            proto.STRING,
            number=2,
        )
        activity_id: int = proto.Field(
            proto.INT64,
            number=3,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=21,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=22,
        optional=True,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=33,
    )
    status: conversion_action_status.ConversionActionStatusEnum.ConversionActionStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=conversion_action_status.ConversionActionStatusEnum.ConversionActionStatus,
    )
    type_: conversion_action_type.ConversionActionTypeEnum.ConversionActionType = proto.Field(
        proto.ENUM,
        number=5,
        enum=conversion_action_type.ConversionActionTypeEnum.ConversionActionType,
    )
    primary_for_goal: bool = proto.Field(
        proto.BOOL,
        number=31,
        optional=True,
    )
    category: conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory = proto.Field(
        proto.ENUM,
        number=6,
        enum=conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    owner_customer: str = proto.Field(
        proto.STRING,
        number=23,
        optional=True,
    )
    include_in_client_account_conversions_metric: bool = proto.Field(
        proto.BOOL,
        number=24,
        optional=True,
    )
    include_in_conversions_metric: bool = proto.Field(
        proto.BOOL,
        number=32,
        optional=True,
    )
    click_through_lookback_window_days: int = proto.Field(
        proto.INT64,
        number=25,
        optional=True,
    )
    value_settings: ValueSettings = proto.Field(
        proto.MESSAGE,
        number=11,
        message=ValueSettings,
    )
    attribution_model_settings: AttributionModelSettings = proto.Field(
        proto.MESSAGE,
        number=13,
        message=AttributionModelSettings,
    )
    app_id: str = proto.Field(
        proto.STRING,
        number=28,
        optional=True,
    )
    floodlight_settings: FloodlightSettings = proto.Field(
        proto.MESSAGE,
        number=29,
        message=FloodlightSettings,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
