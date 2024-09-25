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

from google.ads.searchads360.v0.common.types import ad_type_infos
from google.ads.searchads360.v0.enums.types import ad_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Ad',
    },
)


class Ad(proto.Message):
    r"""An ad.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad. Ad resource names
            have the form:

            ``customers/{customer_id}/ads/{ad_id}``
        id (int):
            Output only. The ID of the ad.

            This field is a member of `oneof`_ ``_id``.
        final_urls (MutableSequence[str]):
            The list of possible final URLs after all
            cross-domain redirects for the ad.
        display_url (str):
            The URL that appears in the ad description
            for some ad formats.

            This field is a member of `oneof`_ ``_display_url``.
        type_ (google.ads.searchads360.v0.enums.types.AdTypeEnum.AdType):
            Output only. The type of ad.
        name (str):
            Immutable. The name of the ad. This is only
            used to be able to identify the ad. It does not
            need to be unique and does not affect the served
            ad. The name field is currently only supported
            for DisplayUploadAd, ImageAd,
            ShoppingComparisonListingAd and VideoAd.

            This field is a member of `oneof`_ ``_name``.
        text_ad (google.ads.searchads360.v0.common.types.SearchAds360TextAdInfo):
            Immutable. Details pertaining to a text ad.

            This field is a member of `oneof`_ ``ad_data``.
        expanded_text_ad (google.ads.searchads360.v0.common.types.SearchAds360ExpandedTextAdInfo):
            Immutable. Details pertaining to an expanded
            text ad.

            This field is a member of `oneof`_ ``ad_data``.
        responsive_search_ad (google.ads.searchads360.v0.common.types.SearchAds360ResponsiveSearchAdInfo):
            Immutable. Details pertaining to a responsive
            search ad.

            This field is a member of `oneof`_ ``ad_data``.
        product_ad (google.ads.searchads360.v0.common.types.SearchAds360ProductAdInfo):
            Immutable. Details pertaining to a product
            ad.

            This field is a member of `oneof`_ ``ad_data``.
        expanded_dynamic_search_ad (google.ads.searchads360.v0.common.types.SearchAds360ExpandedDynamicSearchAdInfo):
            Immutable. Details pertaining to an expanded
            dynamic search ad.

            This field is a member of `oneof`_ ``ad_data``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=37,
    )
    id: int = proto.Field(
        proto.INT64,
        number=40,
        optional=True,
    )
    final_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=41,
    )
    display_url: str = proto.Field(
        proto.STRING,
        number=45,
        optional=True,
    )
    type_: ad_type.AdTypeEnum.AdType = proto.Field(
        proto.ENUM,
        number=5,
        enum=ad_type.AdTypeEnum.AdType,
    )
    name: str = proto.Field(
        proto.STRING,
        number=47,
        optional=True,
    )
    text_ad: ad_type_infos.SearchAds360TextAdInfo = proto.Field(
        proto.MESSAGE,
        number=55,
        oneof='ad_data',
        message=ad_type_infos.SearchAds360TextAdInfo,
    )
    expanded_text_ad: ad_type_infos.SearchAds360ExpandedTextAdInfo = proto.Field(
        proto.MESSAGE,
        number=56,
        oneof='ad_data',
        message=ad_type_infos.SearchAds360ExpandedTextAdInfo,
    )
    responsive_search_ad: ad_type_infos.SearchAds360ResponsiveSearchAdInfo = proto.Field(
        proto.MESSAGE,
        number=57,
        oneof='ad_data',
        message=ad_type_infos.SearchAds360ResponsiveSearchAdInfo,
    )
    product_ad: ad_type_infos.SearchAds360ProductAdInfo = proto.Field(
        proto.MESSAGE,
        number=58,
        oneof='ad_data',
        message=ad_type_infos.SearchAds360ProductAdInfo,
    )
    expanded_dynamic_search_ad: ad_type_infos.SearchAds360ExpandedDynamicSearchAdInfo = proto.Field(
        proto.MESSAGE,
        number=59,
        oneof='ad_data',
        message=ad_type_infos.SearchAds360ExpandedDynamicSearchAdInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
