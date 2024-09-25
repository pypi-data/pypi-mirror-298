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

from google.ads.searchads360.v0.enums.types import custom_column_render_type
from google.ads.searchads360.v0.enums.types import custom_column_value_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'CustomColumn',
    },
)


class CustomColumn(proto.Message):
    r"""A custom column.
    See Search Ads 360 custom column at
    https://support.google.com/sa360/answer/9633916

    Attributes:
        resource_name (str):
            Immutable. The resource name of the custom column. Custom
            column resource names have the form:

            ``customers/{customer_id}/customColumns/{custom_column_id}``
        id (int):
            Output only. ID of the custom column.
        name (str):
            Output only. User-defined name of the custom
            column.
        description (str):
            Output only. User-defined description of the
            custom column.
        value_type (google.ads.searchads360.v0.enums.types.CustomColumnValueTypeEnum.CustomColumnValueType):
            Output only. The type of the result value of
            the custom column.
        references_attributes (bool):
            Output only. True when the custom column is
            referring to one or more attributes.
        references_metrics (bool):
            Output only. True when the custom column is
            referring to one or more metrics.
        queryable (bool):
            Output only. True when the custom column is
            available to be used in the query of
            SearchAds360Service.Search and
            SearchAds360Service.SearchStream.
        referenced_system_columns (MutableSequence[str]):
            Output only. The list of the referenced
            system columns of this custom column. For
            example, A custom column "sum of impressions and
            clicks" has referenced system columns of
            {"metrics.clicks", "metrics.impressions"}.
        render_type (google.ads.searchads360.v0.enums.types.CustomColumnRenderTypeEnum.CustomColumnRenderType):
            Output only. How the result value of the
            custom column should be interpreted.
    """

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
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    value_type: custom_column_value_type.CustomColumnValueTypeEnum.CustomColumnValueType = proto.Field(
        proto.ENUM,
        number=5,
        enum=custom_column_value_type.CustomColumnValueTypeEnum.CustomColumnValueType,
    )
    references_attributes: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    references_metrics: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    queryable: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    referenced_system_columns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    render_type: custom_column_render_type.CustomColumnRenderTypeEnum.CustomColumnRenderType = proto.Field(
        proto.ENUM,
        number=10,
        enum=custom_column_render_type.CustomColumnRenderTypeEnum.CustomColumnRenderType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
