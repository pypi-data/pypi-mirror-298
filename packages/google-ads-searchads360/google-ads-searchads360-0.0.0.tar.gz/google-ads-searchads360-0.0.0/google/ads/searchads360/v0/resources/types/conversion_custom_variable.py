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

from google.ads.searchads360.v0.enums.types import conversion_custom_variable_cardinality
from google.ads.searchads360.v0.enums.types import conversion_custom_variable_family
from google.ads.searchads360.v0.enums.types import conversion_custom_variable_status
from google.ads.searchads360.v0.enums.types import floodlight_variable_data_type as gase_floodlight_variable_data_type
from google.ads.searchads360.v0.enums.types import floodlight_variable_type as gase_floodlight_variable_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'ConversionCustomVariable',
    },
)


class ConversionCustomVariable(proto.Message):
    r"""A conversion custom variable.
    See "About custom Floodlight metrics and dimensions in the new
    Search Ads 360" at
    https://support.google.com/sa360/answer/13567857

    Attributes:
        resource_name (str):
            Immutable. The resource name of the conversion custom
            variable. Conversion custom variable resource names have the
            form:

            ``customers/{customer_id}/conversionCustomVariables/{conversion_custom_variable_id}``
        id (int):
            Output only. The ID of the conversion custom
            variable.
        name (str):
            Required. The name of the conversion custom
            variable. Name should be unique. The maximum
            length of name is 100 characters. There should
            not be any extra spaces before and after.
        tag (str):
            Required. Immutable. The tag of the
            conversion custom variable. Tag should be unique
            and consist of a "u" character directly followed
            with a number less than ormequal to 100. For
            example: "u4".
        status (google.ads.searchads360.v0.enums.types.ConversionCustomVariableStatusEnum.ConversionCustomVariableStatus):
            The status of the conversion custom variable
            for conversion event accrual.
        owner_customer (str):
            Output only. The resource name of the
            customer that owns the conversion custom
            variable.
        family (google.ads.searchads360.v0.enums.types.ConversionCustomVariableFamilyEnum.ConversionCustomVariableFamily):
            Output only. Family of the conversion custom
            variable.
        cardinality (google.ads.searchads360.v0.enums.types.ConversionCustomVariableCardinalityEnum.ConversionCustomVariableCardinality):
            Output only. Cardinality of the conversion
            custom variable.
        floodlight_conversion_custom_variable_info (google.ads.searchads360.v0.resources.types.ConversionCustomVariable.FloodlightConversionCustomVariableInfo):
            Output only. Fields for Search Ads 360
            floodlight conversion custom variables.
        custom_column_ids (MutableSequence[int]):
            Output only. The IDs of custom columns that
            use this conversion custom variable.
    """

    class FloodlightConversionCustomVariableInfo(proto.Message):
        r"""Information for Search Ads 360 Floodlight Conversion Custom
        Variables.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            floodlight_variable_type (google.ads.searchads360.v0.enums.types.FloodlightVariableTypeEnum.FloodlightVariableType):
                Output only. Floodlight variable type defined
                in Search Ads 360.

                This field is a member of `oneof`_ ``_floodlight_variable_type``.
            floodlight_variable_data_type (google.ads.searchads360.v0.enums.types.FloodlightVariableDataTypeEnum.FloodlightVariableDataType):
                Output only. Floodlight variable data type
                defined in Search Ads 360.

                This field is a member of `oneof`_ ``_floodlight_variable_data_type``.
        """

        floodlight_variable_type: gase_floodlight_variable_type.FloodlightVariableTypeEnum.FloodlightVariableType = proto.Field(
            proto.ENUM,
            number=1,
            optional=True,
            enum=gase_floodlight_variable_type.FloodlightVariableTypeEnum.FloodlightVariableType,
        )
        floodlight_variable_data_type: gase_floodlight_variable_data_type.FloodlightVariableDataTypeEnum.FloodlightVariableDataType = proto.Field(
            proto.ENUM,
            number=2,
            optional=True,
            enum=gase_floodlight_variable_data_type.FloodlightVariableDataTypeEnum.FloodlightVariableDataType,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    tag: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status: conversion_custom_variable_status.ConversionCustomVariableStatusEnum.ConversionCustomVariableStatus = proto.Field(
        proto.ENUM,
        number=5,
        enum=conversion_custom_variable_status.ConversionCustomVariableStatusEnum.ConversionCustomVariableStatus,
    )
    owner_customer: str = proto.Field(
        proto.STRING,
        number=6,
    )
    family: conversion_custom_variable_family.ConversionCustomVariableFamilyEnum.ConversionCustomVariableFamily = proto.Field(
        proto.ENUM,
        number=7,
        enum=conversion_custom_variable_family.ConversionCustomVariableFamilyEnum.ConversionCustomVariableFamily,
    )
    cardinality: conversion_custom_variable_cardinality.ConversionCustomVariableCardinalityEnum.ConversionCustomVariableCardinality = proto.Field(
        proto.ENUM,
        number=8,
        enum=conversion_custom_variable_cardinality.ConversionCustomVariableCardinalityEnum.ConversionCustomVariableCardinality,
    )
    floodlight_conversion_custom_variable_info: FloodlightConversionCustomVariableInfo = proto.Field(
        proto.MESSAGE,
        number=9,
        message=FloodlightConversionCustomVariableInfo,
    )
    custom_column_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=10,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
