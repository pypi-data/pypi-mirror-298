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

from google.ads.searchads360.v0.common.types import asset_types
from google.ads.searchads360.v0.enums.types import asset_engine_status
from google.ads.searchads360.v0.enums.types import asset_status
from google.ads.searchads360.v0.enums.types import asset_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Asset',
    },
)


class Asset(proto.Message):
    r"""Asset is a part of an ad which can be shared across multiple
    ads. It can be an image (ImageAsset), a video
    (YoutubeVideoAsset), etc. Assets are immutable and cannot be
    removed. To stop an asset from serving, remove the asset from
    the entity that is using it.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the asset. Asset resource
            names have the form:

            ``customers/{customer_id}/assets/{asset_id}``
        id (int):
            Output only. The ID of the asset.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            Optional name of the asset.

            This field is a member of `oneof`_ ``_name``.
        type_ (google.ads.searchads360.v0.enums.types.AssetTypeEnum.AssetType):
            Output only. Type of the asset.
        final_urls (MutableSequence[str]):
            A list of possible final URLs after all cross
            domain redirects.
        tracking_url_template (str):
            URL template for constructing a tracking URL.

            This field is a member of `oneof`_ ``_tracking_url_template``.
        status (google.ads.searchads360.v0.enums.types.AssetStatusEnum.AssetStatus):
            Output only. The status of the asset.
        creation_time (str):
            Output only. The timestamp when this asset
            was created. The timestamp is in the customer's
            time zone and in "yyyy-MM-dd HH:mm:ss" format.
        last_modified_time (str):
            Output only. The datetime when this asset was
            last modified. The datetime is in the customer's
            time zone and in "yyyy-MM-dd HH:mm:ss.ssssss"
            format.
        engine_status (google.ads.searchads360.v0.enums.types.AssetEngineStatusEnum.AssetEngineStatus):
            Output only. The Engine Status for an asset.

            This field is a member of `oneof`_ ``_engine_status``.
        youtube_video_asset (google.ads.searchads360.v0.common.types.YoutubeVideoAsset):
            Immutable. A YouTube video asset.

            This field is a member of `oneof`_ ``asset_data``.
        image_asset (google.ads.searchads360.v0.common.types.ImageAsset):
            Output only. An image asset.

            This field is a member of `oneof`_ ``asset_data``.
        text_asset (google.ads.searchads360.v0.common.types.TextAsset):
            Output only. A text asset.

            This field is a member of `oneof`_ ``asset_data``.
        callout_asset (google.ads.searchads360.v0.common.types.UnifiedCalloutAsset):
            Output only. A unified callout asset.

            This field is a member of `oneof`_ ``asset_data``.
        sitelink_asset (google.ads.searchads360.v0.common.types.UnifiedSitelinkAsset):
            Output only. A unified sitelink asset.

            This field is a member of `oneof`_ ``asset_data``.
        page_feed_asset (google.ads.searchads360.v0.common.types.UnifiedPageFeedAsset):
            Output only. A unified page feed asset.

            This field is a member of `oneof`_ ``asset_data``.
        mobile_app_asset (google.ads.searchads360.v0.common.types.MobileAppAsset):
            A mobile app asset.

            This field is a member of `oneof`_ ``asset_data``.
        call_asset (google.ads.searchads360.v0.common.types.UnifiedCallAsset):
            Output only. A unified call asset.

            This field is a member of `oneof`_ ``asset_data``.
        call_to_action_asset (google.ads.searchads360.v0.common.types.CallToActionAsset):
            Immutable. A call to action asset.

            This field is a member of `oneof`_ ``asset_data``.
        location_asset (google.ads.searchads360.v0.common.types.UnifiedLocationAsset):
            Output only. A unified location asset.

            This field is a member of `oneof`_ ``asset_data``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=11,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )
    type_: asset_type.AssetTypeEnum.AssetType = proto.Field(
        proto.ENUM,
        number=4,
        enum=asset_type.AssetTypeEnum.AssetType,
    )
    final_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=14,
    )
    tracking_url_template: str = proto.Field(
        proto.STRING,
        number=17,
        optional=True,
    )
    status: asset_status.AssetStatusEnum.AssetStatus = proto.Field(
        proto.ENUM,
        number=42,
        enum=asset_status.AssetStatusEnum.AssetStatus,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=43,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=44,
    )
    engine_status: asset_engine_status.AssetEngineStatusEnum.AssetEngineStatus = proto.Field(
        proto.ENUM,
        number=61,
        optional=True,
        enum=asset_engine_status.AssetEngineStatusEnum.AssetEngineStatus,
    )
    youtube_video_asset: asset_types.YoutubeVideoAsset = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof='asset_data',
        message=asset_types.YoutubeVideoAsset,
    )
    image_asset: asset_types.ImageAsset = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof='asset_data',
        message=asset_types.ImageAsset,
    )
    text_asset: asset_types.TextAsset = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof='asset_data',
        message=asset_types.TextAsset,
    )
    callout_asset: asset_types.UnifiedCalloutAsset = proto.Field(
        proto.MESSAGE,
        number=48,
        oneof='asset_data',
        message=asset_types.UnifiedCalloutAsset,
    )
    sitelink_asset: asset_types.UnifiedSitelinkAsset = proto.Field(
        proto.MESSAGE,
        number=45,
        oneof='asset_data',
        message=asset_types.UnifiedSitelinkAsset,
    )
    page_feed_asset: asset_types.UnifiedPageFeedAsset = proto.Field(
        proto.MESSAGE,
        number=46,
        oneof='asset_data',
        message=asset_types.UnifiedPageFeedAsset,
    )
    mobile_app_asset: asset_types.MobileAppAsset = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof='asset_data',
        message=asset_types.MobileAppAsset,
    )
    call_asset: asset_types.UnifiedCallAsset = proto.Field(
        proto.MESSAGE,
        number=47,
        oneof='asset_data',
        message=asset_types.UnifiedCallAsset,
    )
    call_to_action_asset: asset_types.CallToActionAsset = proto.Field(
        proto.MESSAGE,
        number=29,
        oneof='asset_data',
        message=asset_types.CallToActionAsset,
    )
    location_asset: asset_types.UnifiedLocationAsset = proto.Field(
        proto.MESSAGE,
        number=49,
        oneof='asset_data',
        message=asset_types.UnifiedLocationAsset,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
