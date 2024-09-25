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

from google.ads.searchads360.v0.enums.types import asset_link_status


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'CustomerAsset',
    },
)


class CustomerAsset(proto.Message):
    r"""A link between a customer and an asset.
    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer asset.
            CustomerAsset resource names have the form:

            ``customers/{customer_id}/customerAssets/{asset_id}~{field_type}``
        asset (str):
            Required. Immutable. The asset which is
            linked to the customer.
        status (google.ads.searchads360.v0.enums.types.AssetLinkStatusEnum.AssetLinkStatus):
            Status of the customer asset.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    asset: str = proto.Field(
        proto.STRING,
        number=2,
    )
    status: asset_link_status.AssetLinkStatusEnum.AssetLinkStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=asset_link_status.AssetLinkStatusEnum.AssetLinkStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
