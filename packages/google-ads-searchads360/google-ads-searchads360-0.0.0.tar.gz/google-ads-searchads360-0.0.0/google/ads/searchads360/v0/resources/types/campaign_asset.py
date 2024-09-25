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
        'CampaignAsset',
    },
)


class CampaignAsset(proto.Message):
    r"""A link between a Campaign and an Asset.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign asset.
            CampaignAsset resource names have the form:

            ``customers/{customer_id}/campaignAssets/{campaign_id}~{asset_id}~{field_type}``
        campaign (str):
            Immutable. The campaign to which the asset is
            linked.

            This field is a member of `oneof`_ ``_campaign``.
        asset (str):
            Immutable. The asset which is linked to the
            campaign.

            This field is a member of `oneof`_ ``_asset``.
        status (google.ads.searchads360.v0.enums.types.AssetLinkStatusEnum.AssetLinkStatus):
            Output only. Status of the campaign asset.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    campaign: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    asset: str = proto.Field(
        proto.STRING,
        number=7,
        optional=True,
    )
    status: asset_link_status.AssetLinkStatusEnum.AssetLinkStatus = proto.Field(
        proto.ENUM,
        number=5,
        enum=asset_link_status.AssetLinkStatusEnum.AssetLinkStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
