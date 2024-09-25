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

from google.ads.searchads360.v0.resources.types import custom_column


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.services',
    marshal='google.ads.searchads360.v0',
    manifest={
        'GetCustomColumnRequest',
        'ListCustomColumnsRequest',
        'ListCustomColumnsResponse',
    },
)


class GetCustomColumnRequest(proto.Message):
    r"""Request message for
    [CustomColumnService.GetCustomColumn][google.ads.searchads360.v0.services.CustomColumnService.GetCustomColumn].

    Attributes:
        resource_name (str):
            Required. The resource name of the custom
            column to fetch.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCustomColumnsRequest(proto.Message):
    r"""Request message for
    [CustomColumnService.ListCustomColumns][google.ads.searchads360.v0.services.CustomColumnService.ListCustomColumns]

    Attributes:
        customer_id (str):
            Required. The ID of the customer to apply the
            CustomColumn list operation to.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCustomColumnsResponse(proto.Message):
    r"""Response message for fetching all custom columns associated
    with a customer.

    Attributes:
        custom_columns (MutableSequence[google.ads.searchads360.v0.resources.types.CustomColumn]):
            The CustomColumns owned by the provided
            customer.
    """

    custom_columns: MutableSequence[custom_column.CustomColumn] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=custom_column.CustomColumn,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
