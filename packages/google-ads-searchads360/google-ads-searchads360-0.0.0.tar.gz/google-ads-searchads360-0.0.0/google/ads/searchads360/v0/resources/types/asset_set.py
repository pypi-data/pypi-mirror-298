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


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AssetSet',
    },
)


class AssetSet(proto.Message):
    r"""An asset set representing a collection of assets.
    Use AssetSetAsset to link an asset to the asset set.

    Attributes:
        id (int):
            Output only. The ID of the asset set.
        resource_name (str):
            Immutable. The resource name of the asset set. Asset set
            resource names have the form:

            ``customers/{customer_id}/assetSets/{asset_set_id}``
    """

    id: int = proto.Field(
        proto.INT64,
        number=6,
    )
    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
