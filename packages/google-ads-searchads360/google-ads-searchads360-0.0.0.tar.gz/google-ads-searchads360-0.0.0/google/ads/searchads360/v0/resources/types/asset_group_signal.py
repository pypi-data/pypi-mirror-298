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
        'AssetGroupSignal',
    },
)


class AssetGroupSignal(proto.Message):
    r"""AssetGroupSignal represents a signal in an asset group. The
    existence of a signal tells the performance max campaign who's
    most likely to convert. Performance Max uses the signal to look
    for new people with similar or stronger intent to find
    conversions across Search, Display, Video, and more.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the asset group signal.
            Asset group signal resource name have the form:

            ``customers/{customer_id}/assetGroupSignals/{asset_group_id}~{signal_id}``
        asset_group (str):
            Immutable. The asset group which this asset
            group signal belongs to.
        audience (google.ads.searchads360.v0.common.types.AudienceInfo):
            Immutable. The audience signal to be used by
            the performance max campaign.

            This field is a member of `oneof`_ ``signal``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    asset_group: str = proto.Field(
        proto.STRING,
        number=2,
    )
    audience: criteria.AudienceInfo = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof='signal',
        message=criteria.AudienceInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
