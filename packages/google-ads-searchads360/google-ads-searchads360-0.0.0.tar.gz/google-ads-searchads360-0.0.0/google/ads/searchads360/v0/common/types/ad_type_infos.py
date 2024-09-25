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

from google.ads.searchads360.v0.common.types import ad_asset


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'SearchAds360TextAdInfo',
        'SearchAds360ExpandedTextAdInfo',
        'SearchAds360ExpandedDynamicSearchAdInfo',
        'SearchAds360ProductAdInfo',
        'SearchAds360ResponsiveSearchAdInfo',
    },
)


class SearchAds360TextAdInfo(proto.Message):
    r"""A Search Ads 360 text ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        headline (str):
            The headline of the ad.

            This field is a member of `oneof`_ ``_headline``.
        description1 (str):
            The first line of the ad's description.

            This field is a member of `oneof`_ ``_description1``.
        description2 (str):
            The second line of the ad's description.

            This field is a member of `oneof`_ ``_description2``.
        display_url (str):
            The displayed URL of the ad.

            This field is a member of `oneof`_ ``_display_url``.
        display_mobile_url (str):
            The displayed mobile URL of the ad.

            This field is a member of `oneof`_ ``_display_mobile_url``.
        ad_tracking_id (int):
            The tracking id of the ad.

            This field is a member of `oneof`_ ``_ad_tracking_id``.
    """

    headline: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    description1: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    description2: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    display_url: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    display_mobile_url: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    ad_tracking_id: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )


class SearchAds360ExpandedTextAdInfo(proto.Message):
    r"""A Search Ads 360 expanded text ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        headline (str):
            The headline of the ad.

            This field is a member of `oneof`_ ``_headline``.
        headline2 (str):
            The second headline of the ad.

            This field is a member of `oneof`_ ``_headline2``.
        headline3 (str):
            The third headline of the ad.

            This field is a member of `oneof`_ ``_headline3``.
        description1 (str):
            The first line of the ad's description.

            This field is a member of `oneof`_ ``_description1``.
        description2 (str):
            The second line of the ad's description.

            This field is a member of `oneof`_ ``_description2``.
        path1 (str):
            Text appended to the auto-generated visible
            URL with a delimiter.

            This field is a member of `oneof`_ ``_path1``.
        path2 (str):
            Text appended to path1 with a delimiter.

            This field is a member of `oneof`_ ``_path2``.
        ad_tracking_id (int):
            The tracking id of the ad.

            This field is a member of `oneof`_ ``_ad_tracking_id``.
    """

    headline: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    headline2: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    headline3: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    description1: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    description2: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    path1: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    path2: str = proto.Field(
        proto.STRING,
        number=7,
        optional=True,
    )
    ad_tracking_id: int = proto.Field(
        proto.INT64,
        number=8,
        optional=True,
    )


class SearchAds360ExpandedDynamicSearchAdInfo(proto.Message):
    r"""An expanded dynamic search ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        description1 (str):
            The first line of the ad's description.

            This field is a member of `oneof`_ ``_description1``.
        description2 (str):
            The second line of the ad's description.

            This field is a member of `oneof`_ ``_description2``.
        ad_tracking_id (int):
            The tracking id of the ad.

            This field is a member of `oneof`_ ``_ad_tracking_id``.
    """

    description1: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    description2: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    ad_tracking_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )


class SearchAds360ProductAdInfo(proto.Message):
    r"""A Search Ads 360 product ad.
    """


class SearchAds360ResponsiveSearchAdInfo(proto.Message):
    r"""A Search Ads 360 responsive search ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        path1 (str):
            Text appended to the auto-generated visible
            URL with a delimiter.

            This field is a member of `oneof`_ ``_path1``.
        path2 (str):
            Text appended to path1 with a delimiter.

            This field is a member of `oneof`_ ``_path2``.
        ad_tracking_id (int):
            The tracking id of the ad.

            This field is a member of `oneof`_ ``_ad_tracking_id``.
        headlines (MutableSequence[google.ads.searchads360.v0.common.types.AdTextAsset]):
            List of text assets for headlines. When the
            ad serves the headlines will be selected from
            this list.
        descriptions (MutableSequence[google.ads.searchads360.v0.common.types.AdTextAsset]):
            List of text assets for descriptions. When
            the ad serves the descriptions will be selected
            from this list.
    """

    path1: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    path2: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    ad_tracking_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    headlines: MutableSequence[ad_asset.AdTextAsset] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=ad_asset.AdTextAsset,
    )
    descriptions: MutableSequence[ad_asset.AdTextAsset] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=ad_asset.AdTextAsset,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
