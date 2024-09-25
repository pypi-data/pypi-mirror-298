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
from google.ads.searchads360.v0.enums.types import call_conversion_reporting_state as gase_call_conversion_reporting_state
from google.ads.searchads360.v0.enums.types import call_to_action_type
from google.ads.searchads360.v0.enums.types import location_ownership_type as gase_location_ownership_type
from google.ads.searchads360.v0.enums.types import mime_type as gase_mime_type
from google.ads.searchads360.v0.enums.types import mobile_app_vendor


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'YoutubeVideoAsset',
        'ImageAsset',
        'ImageDimension',
        'TextAsset',
        'UnifiedCalloutAsset',
        'UnifiedSitelinkAsset',
        'UnifiedPageFeedAsset',
        'MobileAppAsset',
        'UnifiedCallAsset',
        'CallToActionAsset',
        'UnifiedLocationAsset',
        'BusinessProfileLocation',
    },
)


class YoutubeVideoAsset(proto.Message):
    r"""A YouTube asset.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        youtube_video_id (str):
            YouTube video id. This is the 11 character
            string value used in the YouTube video URL.

            This field is a member of `oneof`_ ``_youtube_video_id``.
        youtube_video_title (str):
            YouTube video title.
    """

    youtube_video_id: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    youtube_video_title: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ImageAsset(proto.Message):
    r"""An Image asset.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        file_size (int):
            File size of the image asset in bytes.

            This field is a member of `oneof`_ ``_file_size``.
        mime_type (google.ads.searchads360.v0.enums.types.MimeTypeEnum.MimeType):
            MIME type of the image asset.
        full_size (google.ads.searchads360.v0.common.types.ImageDimension):
            Metadata for this image at its original size.
    """

    file_size: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )
    mime_type: gase_mime_type.MimeTypeEnum.MimeType = proto.Field(
        proto.ENUM,
        number=3,
        enum=gase_mime_type.MimeTypeEnum.MimeType,
    )
    full_size: 'ImageDimension' = proto.Field(
        proto.MESSAGE,
        number=4,
        message='ImageDimension',
    )


class ImageDimension(proto.Message):
    r"""Metadata for an image at a certain size, either original or
    resized.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        height_pixels (int):
            Height of the image.

            This field is a member of `oneof`_ ``_height_pixels``.
        width_pixels (int):
            Width of the image.

            This field is a member of `oneof`_ ``_width_pixels``.
        url (str):
            A URL that returns the image with this height
            and width.

            This field is a member of `oneof`_ ``_url``.
    """

    height_pixels: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    width_pixels: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    url: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )


class TextAsset(proto.Message):
    r"""A Text asset.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            Text content of the text asset.

            This field is a member of `oneof`_ ``_text``.
    """

    text: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class UnifiedCalloutAsset(proto.Message):
    r"""A unified callout asset.
    Attributes:
        callout_text (str):
            The callout text.
            The length of this string should be between 1
            and 25, inclusive.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
        ad_schedule_targets (MutableSequence[google.ads.searchads360.v0.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
        use_searcher_time_zone (bool):
            Whether to show the asset in search user's
            time zone. Applies to Microsoft Ads.
    """

    callout_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=2,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=3,
    )
    ad_schedule_targets: MutableSequence[criteria.AdScheduleInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=criteria.AdScheduleInfo,
    )
    use_searcher_time_zone: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UnifiedSitelinkAsset(proto.Message):
    r"""A unified sitelink asset.
    Attributes:
        link_text (str):
            URL display text for the sitelink.
            The length of this string should be between 1
            and 25, inclusive.
        description1 (str):
            First line of the description for the
            sitelink. If set, the length should be between 1
            and 35, inclusive, and description2 must also be
            set.
        description2 (str):
            Second line of the description for the
            sitelink. If set, the length should be between 1
            and 35, inclusive, and description1 must also be
            set.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
        ad_schedule_targets (MutableSequence[google.ads.searchads360.v0.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
        tracking_id (int):
            ID used for tracking clicks for the sitelink
            asset. This is a Yahoo! Japan only field.
        use_searcher_time_zone (bool):
            Whether to show the sitelink asset in search
            user's time zone. Applies to Microsoft Ads.
        mobile_preferred (bool):
            Whether the preference is for the sitelink
            asset to be displayed on mobile devices. Applies
            to Microsoft Ads.
    """

    link_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description1: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description2: str = proto.Field(
        proto.STRING,
        number=3,
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=4,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=5,
    )
    ad_schedule_targets: MutableSequence[criteria.AdScheduleInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=criteria.AdScheduleInfo,
    )
    tracking_id: int = proto.Field(
        proto.INT64,
        number=7,
    )
    use_searcher_time_zone: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    mobile_preferred: bool = proto.Field(
        proto.BOOL,
        number=9,
    )


class UnifiedPageFeedAsset(proto.Message):
    r"""A Unified Page Feed asset.
    Attributes:
        page_url (str):
            The webpage that advertisers want to target.
        labels (MutableSequence[str]):
            Labels used to group the page urls.
    """

    page_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class MobileAppAsset(proto.Message):
    r"""An asset representing a mobile app.
    Attributes:
        app_id (str):
            Required. A string that uniquely identifies a
            mobile application. It should just contain the
            platform native id, like "com.android.ebay" for
            Android or "12345689" for iOS.
        app_store (google.ads.searchads360.v0.enums.types.MobileAppVendorEnum.MobileAppVendor):
            Required. The application store that
            distributes this specific app.
    """

    app_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    app_store: mobile_app_vendor.MobileAppVendorEnum.MobileAppVendor = proto.Field(
        proto.ENUM,
        number=2,
        enum=mobile_app_vendor.MobileAppVendorEnum.MobileAppVendor,
    )


class UnifiedCallAsset(proto.Message):
    r"""A unified call asset.
    Attributes:
        country_code (str):
            Two-letter country code of the phone number.
            Examples: 'US', 'us'.
        phone_number (str):
            The advertiser's raw phone number. Examples:
            '1234567890', '(123)456-7890'
        call_conversion_reporting_state (google.ads.searchads360.v0.enums.types.CallConversionReportingStateEnum.CallConversionReportingState):
            Output only. Indicates whether this CallAsset
            should use its own call conversion setting,
            follow the account level setting, or disable
            call conversion.
        call_conversion_action (str):
            The conversion action to attribute a call conversion to. If
            not set, the default conversion action is used. This field
            only has effect if call_conversion_reporting_state is set to
            USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION.
        ad_schedule_targets (MutableSequence[google.ads.searchads360.v0.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
        call_only (bool):
            Whether the call only shows the phone number
            without a link to the website. Applies to
            Microsoft Ads.
        call_tracking_enabled (bool):
            Whether the call should be enabled on call
            tracking. Applies to Microsoft Ads.
        use_searcher_time_zone (bool):
            Whether to show the call extension in search
            user's time zone. Applies to Microsoft Ads.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
    """

    country_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phone_number: str = proto.Field(
        proto.STRING,
        number=2,
    )
    call_conversion_reporting_state: gase_call_conversion_reporting_state.CallConversionReportingStateEnum.CallConversionReportingState = proto.Field(
        proto.ENUM,
        number=3,
        enum=gase_call_conversion_reporting_state.CallConversionReportingStateEnum.CallConversionReportingState,
    )
    call_conversion_action: str = proto.Field(
        proto.STRING,
        number=4,
    )
    ad_schedule_targets: MutableSequence[criteria.AdScheduleInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=criteria.AdScheduleInfo,
    )
    call_only: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    call_tracking_enabled: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    use_searcher_time_zone: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=10,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=11,
    )


class CallToActionAsset(proto.Message):
    r"""A call to action asset.
    Attributes:
        call_to_action (google.ads.searchads360.v0.enums.types.CallToActionTypeEnum.CallToActionType):
            Call to action.
    """

    call_to_action: call_to_action_type.CallToActionTypeEnum.CallToActionType = proto.Field(
        proto.ENUM,
        number=1,
        enum=call_to_action_type.CallToActionTypeEnum.CallToActionType,
    )


class UnifiedLocationAsset(proto.Message):
    r"""A unified location asset.
    Attributes:
        place_id (str):
            Place IDs uniquely identify a place in the
            Google Places database and on Google Maps.
            This field is unique for a given customer ID and
            asset type. See
            https://developers.google.com/places/web-service/place-id
            to learn more about Place ID.
        business_profile_locations (MutableSequence[google.ads.searchads360.v0.common.types.BusinessProfileLocation]):
            The list of business locations for the
            customer. This will only be returned if the
            Location Asset is syncing from the Business
            Profile account. It is possible to have multiple
            Business Profile listings under the same account
            that point to the same Place ID.
        location_ownership_type (google.ads.searchads360.v0.enums.types.LocationOwnershipTypeEnum.LocationOwnershipType):
            The type of location ownership. If the type is
            BUSINESS_OWNER, it will be served as a location extension.
            If the type is AFFILIATE, it will be served as an affiliate
            location.
    """

    place_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    business_profile_locations: MutableSequence['BusinessProfileLocation'] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message='BusinessProfileLocation',
    )
    location_ownership_type: gase_location_ownership_type.LocationOwnershipTypeEnum.LocationOwnershipType = proto.Field(
        proto.ENUM,
        number=3,
        enum=gase_location_ownership_type.LocationOwnershipTypeEnum.LocationOwnershipType,
    )


class BusinessProfileLocation(proto.Message):
    r"""Business Profile location data synced from the linked
    Business Profile account.

    Attributes:
        labels (MutableSequence[str]):
            Advertiser specified label for the location
            on the Business Profile account. This is synced
            from the Business Profile account.
        store_code (str):
            Business Profile store code of this location.
            This is synced from the Business Profile
            account.
        listing_id (int):
            Listing ID of this Business Profile location.
            This is synced from the linked Business Profile
            account.
    """

    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    store_code: str = proto.Field(
        proto.STRING,
        number=2,
    )
    listing_id: int = proto.Field(
        proto.INT64,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
