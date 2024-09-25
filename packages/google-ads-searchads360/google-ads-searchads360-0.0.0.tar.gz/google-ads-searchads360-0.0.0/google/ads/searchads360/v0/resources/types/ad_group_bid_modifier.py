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


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AdGroupBidModifier',
    },
)


class AdGroupBidModifier(proto.Message):
    r"""Represents an ad group bid modifier.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group bid modifier.
            Ad group bid modifier resource names have the form:

            ``customers/{customer_id}/adGroupBidModifiers/{ad_group_id}~{criterion_id}``
        bid_modifier (float):
            The modifier for the bid when the criterion
            matches. The modifier must be in the range: 0.1
            - 10.0. The range is 1.0 - 6.0 for
            PreferredContent. Use 0 to opt out of a Device
            type.

            This field is a member of `oneof`_ ``_bid_modifier``.
        device (google.ads.searchads360.v0.common.types.DeviceInfo):
            Immutable. A device criterion.

            This field is a member of `oneof`_ ``criterion``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    bid_modifier: float = proto.Field(
        proto.DOUBLE,
        number=15,
        optional=True,
    )
    device: criteria.DeviceInfo = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof='criterion',
        message=criteria.DeviceInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
