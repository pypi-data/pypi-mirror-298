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

from google.ads.searchads360.v0.enums.types import targeting_dimension as gase_targeting_dimension


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'TargetingSetting',
        'TargetRestriction',
    },
)


class TargetingSetting(proto.Message):
    r"""Settings for the targeting-related features, at the campaign
    and ad group levels. For more details about the targeting
    setting, visit
    https://support.google.com/google-ads/answer/7365594

    Attributes:
        target_restrictions (MutableSequence[google.ads.searchads360.v0.common.types.TargetRestriction]):
            The per-targeting-dimension setting to
            restrict the reach of your campaign or ad group.
    """

    target_restrictions: MutableSequence['TargetRestriction'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='TargetRestriction',
    )


class TargetRestriction(proto.Message):
    r"""The list of per-targeting-dimension targeting settings.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        targeting_dimension (google.ads.searchads360.v0.enums.types.TargetingDimensionEnum.TargetingDimension):
            The targeting dimension that these settings
            apply to.
        bid_only (bool):
            Indicates whether to restrict your ads to show only for the
            criteria you have selected for this targeting_dimension, or
            to target all values for this targeting_dimension and show
            ads based on your targeting in other TargetingDimensions. A
            value of ``true`` means that these criteria will only apply
            bid modifiers, and not affect targeting. A value of
            ``false`` means that these criteria will restrict targeting
            as well as applying bid modifiers.

            This field is a member of `oneof`_ ``_bid_only``.
    """

    targeting_dimension: gase_targeting_dimension.TargetingDimensionEnum.TargetingDimension = proto.Field(
        proto.ENUM,
        number=1,
        enum=gase_targeting_dimension.TargetingDimensionEnum.TargetingDimension,
    )
    bid_only: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
