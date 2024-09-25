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

from google.ads.searchads360.v0.common.types import bidding
from google.ads.searchads360.v0.common.types import custom_parameter
from google.ads.searchads360.v0.common.types import frequency_cap
from google.ads.searchads360.v0.common.types import real_time_bidding_setting as gasc_real_time_bidding_setting
from google.ads.searchads360.v0.enums.types import ad_serving_optimization_status as gase_ad_serving_optimization_status
from google.ads.searchads360.v0.enums.types import advertising_channel_sub_type as gase_advertising_channel_sub_type
from google.ads.searchads360.v0.enums.types import advertising_channel_type as gase_advertising_channel_type
from google.ads.searchads360.v0.enums.types import asset_field_type
from google.ads.searchads360.v0.enums.types import bidding_strategy_system_status as gase_bidding_strategy_system_status
from google.ads.searchads360.v0.enums.types import bidding_strategy_type as gase_bidding_strategy_type
from google.ads.searchads360.v0.enums.types import campaign_serving_status
from google.ads.searchads360.v0.enums.types import campaign_status
from google.ads.searchads360.v0.enums.types import negative_geo_target_type as gase_negative_geo_target_type
from google.ads.searchads360.v0.enums.types import optimization_goal_type
from google.ads.searchads360.v0.enums.types import positive_geo_target_type as gase_positive_geo_target_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Campaign',
    },
)


class Campaign(proto.Message):
    r"""A campaign.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign. Campaign
            resource names have the form:

            ``customers/{customer_id}/campaigns/{campaign_id}``
        id (int):
            Output only. The ID of the campaign.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            The name of the campaign.

            This field is required and should not be empty
            when creating new campaigns.

            It must not contain any null (code point 0x0),
            NL line feed (code point 0xA) or carriage return
            (code point 0xD) characters.

            This field is a member of `oneof`_ ``_name``.
        status (google.ads.searchads360.v0.enums.types.CampaignStatusEnum.CampaignStatus):
            The status of the campaign.

            When a new campaign is added, the status
            defaults to ENABLED.
        serving_status (google.ads.searchads360.v0.enums.types.CampaignServingStatusEnum.CampaignServingStatus):
            Output only. The ad serving status of the
            campaign.
        bidding_strategy_system_status (google.ads.searchads360.v0.enums.types.BiddingStrategySystemStatusEnum.BiddingStrategySystemStatus):
            Output only. The system status of the
            campaign's bidding strategy.
        ad_serving_optimization_status (google.ads.searchads360.v0.enums.types.AdServingOptimizationStatusEnum.AdServingOptimizationStatus):
            The ad serving optimization status of the
            campaign.
        advertising_channel_type (google.ads.searchads360.v0.enums.types.AdvertisingChannelTypeEnum.AdvertisingChannelType):
            Immutable. The primary serving target for ads within the
            campaign. The targeting options can be refined in
            ``network_settings``.

            This field is required and should not be empty when creating
            new campaigns.

            Can be set only when creating campaigns. After the campaign
            is created, the field can not be changed.
        advertising_channel_sub_type (google.ads.searchads360.v0.enums.types.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType):
            Immutable. Optional refinement to
            ``advertising_channel_type``. Must be a valid sub-type of
            the parent channel type.

            Can be set only when creating campaigns. After campaign is
            created, the field can not be changed.
        tracking_url_template (str):
            The URL template for constructing a tracking
            URL.

            This field is a member of `oneof`_ ``_tracking_url_template``.
        url_custom_parameters (MutableSequence[google.ads.searchads360.v0.common.types.CustomParameter]):
            The list of mappings used to substitute custom parameter
            tags in a ``tracking_url_template``, ``final_urls``, or
            ``mobile_final_urls``.
        real_time_bidding_setting (google.ads.searchads360.v0.common.types.RealTimeBiddingSetting):
            Settings for Real-Time Bidding, a feature
            only available for campaigns targeting the Ad
            Exchange network.
        network_settings (google.ads.searchads360.v0.resources.types.Campaign.NetworkSettings):
            The network settings for the campaign.
        dynamic_search_ads_setting (google.ads.searchads360.v0.resources.types.Campaign.DynamicSearchAdsSetting):
            The setting for controlling Dynamic Search
            Ads (DSA).
        shopping_setting (google.ads.searchads360.v0.resources.types.Campaign.ShoppingSetting):
            The setting for controlling Shopping
            campaigns.
        geo_target_type_setting (google.ads.searchads360.v0.resources.types.Campaign.GeoTargetTypeSetting):
            The setting for ads geotargeting.
        labels (MutableSequence[str]):
            Output only. The resource names of labels
            attached to this campaign.
        campaign_budget (str):
            The budget of the campaign.

            This field is a member of `oneof`_ ``_campaign_budget``.
        bidding_strategy_type (google.ads.searchads360.v0.enums.types.BiddingStrategyTypeEnum.BiddingStrategyType):
            Output only. The type of bidding strategy.

            A bidding strategy can be created by setting either the
            bidding scheme to create a standard bidding strategy or the
            ``bidding_strategy`` field to create a portfolio bidding
            strategy.

            This field is read-only.
        accessible_bidding_strategy (str):
            Output only. Resource name of AccessibleBiddingStrategy, a
            read-only view of the unrestricted attributes of the
            attached portfolio bidding strategy identified by
            'bidding_strategy'. Empty, if the campaign does not use a
            portfolio strategy. Unrestricted strategy attributes are
            available to all customers with whom the strategy is shared
            and are read from the AccessibleBiddingStrategy resource. In
            contrast, restricted attributes are only available to the
            owner customer of the strategy and their managers.
            Restricted attributes can only be read from the
            BiddingStrategy resource.
        start_date (str):
            The date when campaign started in serving
            customer's timezone in YYYY-MM-DD format.

            This field is a member of `oneof`_ ``_start_date``.
        end_date (str):
            The last day of the campaign in serving
            customer's timezone in YYYY-MM-DD format. On
            create, defaults to 2037-12-30, which means the
            campaign will run indefinitely. To set an
            existing campaign to run indefinitely, set this
            field to 2037-12-30.

            This field is a member of `oneof`_ ``_end_date``.
        final_url_suffix (str):
            Suffix used to append query parameters to
            landing pages that are served with parallel
            tracking.

            This field is a member of `oneof`_ ``_final_url_suffix``.
        frequency_caps (MutableSequence[google.ads.searchads360.v0.common.types.FrequencyCapEntry]):
            A list that limits how often each user will
            see this campaign's ads.
        selective_optimization (google.ads.searchads360.v0.resources.types.Campaign.SelectiveOptimization):
            Selective optimization setting for this campaign, which
            includes a set of conversion actions to optimize this
            campaign towards. This feature only applies to app campaigns
            that use MULTI_CHANNEL as AdvertisingChannelType and
            APP_CAMPAIGN or APP_CAMPAIGN_FOR_ENGAGEMENT as
            AdvertisingChannelSubType.
        optimization_goal_setting (google.ads.searchads360.v0.resources.types.Campaign.OptimizationGoalSetting):
            Optimization goal setting for this campaign,
            which includes a set of optimization goal types.
        tracking_setting (google.ads.searchads360.v0.resources.types.Campaign.TrackingSetting):
            Output only. Campaign-level settings for
            tracking information.
        engine_id (str):
            Output only. ID of the campaign in the
            external engine account. This field is for
            non-Google Ads account only, for example, Yahoo
            Japan, Microsoft, Baidu etc. For Google Ads
            entity, use "campaign.id" instead.
        excluded_parent_asset_field_types (MutableSequence[google.ads.searchads360.v0.enums.types.AssetFieldTypeEnum.AssetFieldType]):
            The asset field types that should be excluded
            from this campaign. Asset links with these field
            types will not be inherited by this campaign
            from the upper level.
        create_time (str):
            Output only. The timestamp when this campaign was created.
            The timestamp is in the customer's time zone and in
            "yyyy-MM-dd HH:mm:ss" format. create_time will be deprecated
            in v1. Use creation_time instead.
        creation_time (str):
            Output only. The timestamp when this campaign
            was created. The timestamp is in the customer's
            time zone and in "yyyy-MM-dd HH:mm:ss" format.
        last_modified_time (str):
            Output only. The datetime when this campaign
            was last modified. The datetime is in the
            customer's time zone and in "yyyy-MM-dd
            HH:mm:ss.ssssss" format.
        url_expansion_opt_out (bool):
            Represents opting out of URL expansion to
            more targeted URLs. If opted out (true), only
            the final URLs in the asset group or URLs
            specified in the advertiser's Google Merchant
            Center or business data feeds are targeted. If
            opted in (false), the entire domain will be
            targeted. This field can only be set for
            Performance Max campaigns, where the default
            value is false.

            This field is a member of `oneof`_ ``_url_expansion_opt_out``.
        bidding_strategy (str):
            Portfolio bidding strategy used by campaign.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        manual_cpa (google.ads.searchads360.v0.common.types.ManualCpa):
            Standard Manual CPA bidding strategy.
            Manual bidding strategy that allows advertiser
            to set the bid per advertiser-specified action.
            Supported only for Local Services campaigns.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        manual_cpc (google.ads.searchads360.v0.common.types.ManualCpc):
            Standard Manual CPC bidding strategy.
            Manual click-based bidding where user pays per
            click.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        manual_cpm (google.ads.searchads360.v0.common.types.ManualCpm):
            Standard Manual CPM bidding strategy.
            Manual impression-based bidding where user pays
            per thousand impressions.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        maximize_conversions (google.ads.searchads360.v0.common.types.MaximizeConversions):
            Standard Maximize Conversions bidding
            strategy that automatically maximizes number of
            conversions while spending your budget.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        maximize_conversion_value (google.ads.searchads360.v0.common.types.MaximizeConversionValue):
            Standard Maximize Conversion Value bidding
            strategy that automatically sets bids to
            maximize revenue while spending your budget.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        target_cpa (google.ads.searchads360.v0.common.types.TargetCpa):
            Standard Target CPA bidding strategy that
            automatically sets bids to help get as many
            conversions as possible at the target
            cost-per-acquisition (CPA) you set.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        target_impression_share (google.ads.searchads360.v0.common.types.TargetImpressionShare):
            Target Impression Share bidding strategy. An
            automated bidding strategy that sets bids to
            achieve a chosen percentage of impressions.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        target_roas (google.ads.searchads360.v0.common.types.TargetRoas):
            Standard Target ROAS bidding strategy that
            automatically maximizes revenue while averaging
            a specific target return on ad spend (ROAS).

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        target_spend (google.ads.searchads360.v0.common.types.TargetSpend):
            Standard Target Spend bidding strategy that
            automatically sets your bids to help get as many
            clicks as possible within your budget.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        percent_cpc (google.ads.searchads360.v0.common.types.PercentCpc):
            Standard Percent Cpc bidding strategy where
            bids are a fraction of the advertised price for
            some good or service.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
        target_cpm (google.ads.searchads360.v0.common.types.TargetCpm):
            A bidding strategy that automatically
            optimizes cost per thousand impressions.

            This field is a member of `oneof`_ ``campaign_bidding_strategy``.
    """

    class NetworkSettings(proto.Message):
        r"""The network settings for the campaign.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            target_google_search (bool):
                Whether ads will be served with google.com
                search results.

                This field is a member of `oneof`_ ``_target_google_search``.
            target_search_network (bool):
                Whether ads will be served on partner sites in the Google
                Search Network (requires ``target_google_search`` to also be
                ``true``).

                This field is a member of `oneof`_ ``_target_search_network``.
            target_content_network (bool):
                Whether ads will be served on specified
                placements in the Google Display Network.
                Placements are specified using the Placement
                criterion.

                This field is a member of `oneof`_ ``_target_content_network``.
            target_partner_search_network (bool):
                Whether ads will be served on the Google
                Partner Network. This is available only to some
                select Google partner accounts.

                This field is a member of `oneof`_ ``_target_partner_search_network``.
        """

        target_google_search: bool = proto.Field(
            proto.BOOL,
            number=5,
            optional=True,
        )
        target_search_network: bool = proto.Field(
            proto.BOOL,
            number=6,
            optional=True,
        )
        target_content_network: bool = proto.Field(
            proto.BOOL,
            number=7,
            optional=True,
        )
        target_partner_search_network: bool = proto.Field(
            proto.BOOL,
            number=8,
            optional=True,
        )

    class DynamicSearchAdsSetting(proto.Message):
        r"""The setting for controlling Dynamic Search Ads (DSA).
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            domain_name (str):
                Required. The Internet domain name that this
                setting represents, for example, "google.com" or
                "www.google.com".
            language_code (str):
                Required. The language code specifying the
                language of the domain, for example, "en".
            use_supplied_urls_only (bool):
                Whether the campaign uses advertiser supplied
                URLs exclusively.

                This field is a member of `oneof`_ ``_use_supplied_urls_only``.
        """

        domain_name: str = proto.Field(
            proto.STRING,
            number=6,
        )
        language_code: str = proto.Field(
            proto.STRING,
            number=7,
        )
        use_supplied_urls_only: bool = proto.Field(
            proto.BOOL,
            number=8,
            optional=True,
        )

    class ShoppingSetting(proto.Message):
        r"""The setting for Shopping campaigns. Defines the universe of
        products that can be advertised by the campaign, and how this
        campaign interacts with other Shopping campaigns.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            merchant_id (int):
                Immutable. ID of the Merchant Center account.
                This field is required for create operations.
                This field is immutable for Shopping campaigns.

                This field is a member of `oneof`_ ``_merchant_id``.
            sales_country (str):
                Sales country of products to include in the
                campaign.

                This field is a member of `oneof`_ ``_sales_country``.
            feed_label (str):
                Feed label of products to include in the campaign. Only one
                of feed_label or sales_country can be set. If used instead
                of sales_country, the feed_label field accepts country codes
                in the same format for example: 'XX'. Otherwise can be any
                string used for feed label in Google Merchant Center.
            campaign_priority (int):
                Priority of the campaign. Campaigns with
                numerically higher priorities take precedence
                over those with lower priorities. This field is
                required for Shopping campaigns, with values
                between 0 and 2, inclusive.
                This field is optional for Smart Shopping
                campaigns, but must be equal to 3 if set.

                This field is a member of `oneof`_ ``_campaign_priority``.
            enable_local (bool):
                Whether to include local products.

                This field is a member of `oneof`_ ``_enable_local``.
            use_vehicle_inventory (bool):
                Immutable. Whether to target Vehicle Listing
                inventory.
        """

        merchant_id: int = proto.Field(
            proto.INT64,
            number=5,
            optional=True,
        )
        sales_country: str = proto.Field(
            proto.STRING,
            number=6,
            optional=True,
        )
        feed_label: str = proto.Field(
            proto.STRING,
            number=10,
        )
        campaign_priority: int = proto.Field(
            proto.INT32,
            number=7,
            optional=True,
        )
        enable_local: bool = proto.Field(
            proto.BOOL,
            number=8,
            optional=True,
        )
        use_vehicle_inventory: bool = proto.Field(
            proto.BOOL,
            number=9,
        )

    class TrackingSetting(proto.Message):
        r"""Campaign-level settings for tracking information.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            tracking_url (str):
                Output only. The url used for dynamic
                tracking.

                This field is a member of `oneof`_ ``_tracking_url``.
        """

        tracking_url: str = proto.Field(
            proto.STRING,
            number=2,
            optional=True,
        )

    class GeoTargetTypeSetting(proto.Message):
        r"""Represents a collection of settings related to ads
        geotargeting.

        Attributes:
            positive_geo_target_type (google.ads.searchads360.v0.enums.types.PositiveGeoTargetTypeEnum.PositiveGeoTargetType):
                The setting used for positive geotargeting in
                this particular campaign.
            negative_geo_target_type (google.ads.searchads360.v0.enums.types.NegativeGeoTargetTypeEnum.NegativeGeoTargetType):
                The setting used for negative geotargeting in
                this particular campaign.
        """

        positive_geo_target_type: gase_positive_geo_target_type.PositiveGeoTargetTypeEnum.PositiveGeoTargetType = proto.Field(
            proto.ENUM,
            number=1,
            enum=gase_positive_geo_target_type.PositiveGeoTargetTypeEnum.PositiveGeoTargetType,
        )
        negative_geo_target_type: gase_negative_geo_target_type.NegativeGeoTargetTypeEnum.NegativeGeoTargetType = proto.Field(
            proto.ENUM,
            number=2,
            enum=gase_negative_geo_target_type.NegativeGeoTargetTypeEnum.NegativeGeoTargetType,
        )

    class SelectiveOptimization(proto.Message):
        r"""Selective optimization setting for this campaign, which includes a
        set of conversion actions to optimize this campaign towards. This
        feature only applies to app campaigns that use MULTI_CHANNEL as
        AdvertisingChannelType and APP_CAMPAIGN or
        APP_CAMPAIGN_FOR_ENGAGEMENT as AdvertisingChannelSubType.

        Attributes:
            conversion_actions (MutableSequence[str]):
                The selected set of conversion actions for
                optimizing this campaign.
        """

        conversion_actions: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class OptimizationGoalSetting(proto.Message):
        r"""Optimization goal setting for this campaign, which includes a
        set of optimization goal types.

        Attributes:
            optimization_goal_types (MutableSequence[google.ads.searchads360.v0.enums.types.OptimizationGoalTypeEnum.OptimizationGoalType]):
                The list of optimization goal types.
        """

        optimization_goal_types: MutableSequence[optimization_goal_type.OptimizationGoalTypeEnum.OptimizationGoalType] = proto.RepeatedField(
            proto.ENUM,
            number=1,
            enum=optimization_goal_type.OptimizationGoalTypeEnum.OptimizationGoalType,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=59,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=58,
        optional=True,
    )
    status: campaign_status.CampaignStatusEnum.CampaignStatus = proto.Field(
        proto.ENUM,
        number=5,
        enum=campaign_status.CampaignStatusEnum.CampaignStatus,
    )
    serving_status: campaign_serving_status.CampaignServingStatusEnum.CampaignServingStatus = proto.Field(
        proto.ENUM,
        number=21,
        enum=campaign_serving_status.CampaignServingStatusEnum.CampaignServingStatus,
    )
    bidding_strategy_system_status: gase_bidding_strategy_system_status.BiddingStrategySystemStatusEnum.BiddingStrategySystemStatus = proto.Field(
        proto.ENUM,
        number=78,
        enum=gase_bidding_strategy_system_status.BiddingStrategySystemStatusEnum.BiddingStrategySystemStatus,
    )
    ad_serving_optimization_status: gase_ad_serving_optimization_status.AdServingOptimizationStatusEnum.AdServingOptimizationStatus = proto.Field(
        proto.ENUM,
        number=8,
        enum=gase_ad_serving_optimization_status.AdServingOptimizationStatusEnum.AdServingOptimizationStatus,
    )
    advertising_channel_type: gase_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType = proto.Field(
        proto.ENUM,
        number=9,
        enum=gase_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType,
    )
    advertising_channel_sub_type: gase_advertising_channel_sub_type.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType = proto.Field(
        proto.ENUM,
        number=10,
        enum=gase_advertising_channel_sub_type.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType,
    )
    tracking_url_template: str = proto.Field(
        proto.STRING,
        number=60,
        optional=True,
    )
    url_custom_parameters: MutableSequence[custom_parameter.CustomParameter] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message=custom_parameter.CustomParameter,
    )
    real_time_bidding_setting: gasc_real_time_bidding_setting.RealTimeBiddingSetting = proto.Field(
        proto.MESSAGE,
        number=39,
        message=gasc_real_time_bidding_setting.RealTimeBiddingSetting,
    )
    network_settings: NetworkSettings = proto.Field(
        proto.MESSAGE,
        number=14,
        message=NetworkSettings,
    )
    dynamic_search_ads_setting: DynamicSearchAdsSetting = proto.Field(
        proto.MESSAGE,
        number=33,
        message=DynamicSearchAdsSetting,
    )
    shopping_setting: ShoppingSetting = proto.Field(
        proto.MESSAGE,
        number=36,
        message=ShoppingSetting,
    )
    geo_target_type_setting: GeoTargetTypeSetting = proto.Field(
        proto.MESSAGE,
        number=47,
        message=GeoTargetTypeSetting,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=61,
    )
    campaign_budget: str = proto.Field(
        proto.STRING,
        number=62,
        optional=True,
    )
    bidding_strategy_type: gase_bidding_strategy_type.BiddingStrategyTypeEnum.BiddingStrategyType = proto.Field(
        proto.ENUM,
        number=22,
        enum=gase_bidding_strategy_type.BiddingStrategyTypeEnum.BiddingStrategyType,
    )
    accessible_bidding_strategy: str = proto.Field(
        proto.STRING,
        number=71,
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=63,
        optional=True,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=64,
        optional=True,
    )
    final_url_suffix: str = proto.Field(
        proto.STRING,
        number=65,
        optional=True,
    )
    frequency_caps: MutableSequence[frequency_cap.FrequencyCapEntry] = proto.RepeatedField(
        proto.MESSAGE,
        number=40,
        message=frequency_cap.FrequencyCapEntry,
    )
    selective_optimization: SelectiveOptimization = proto.Field(
        proto.MESSAGE,
        number=45,
        message=SelectiveOptimization,
    )
    optimization_goal_setting: OptimizationGoalSetting = proto.Field(
        proto.MESSAGE,
        number=54,
        message=OptimizationGoalSetting,
    )
    tracking_setting: TrackingSetting = proto.Field(
        proto.MESSAGE,
        number=46,
        message=TrackingSetting,
    )
    engine_id: str = proto.Field(
        proto.STRING,
        number=68,
    )
    excluded_parent_asset_field_types: MutableSequence[asset_field_type.AssetFieldTypeEnum.AssetFieldType] = proto.RepeatedField(
        proto.ENUM,
        number=69,
        enum=asset_field_type.AssetFieldTypeEnum.AssetFieldType,
    )
    create_time: str = proto.Field(
        proto.STRING,
        number=79,
    )
    creation_time: str = proto.Field(
        proto.STRING,
        number=84,
    )
    last_modified_time: str = proto.Field(
        proto.STRING,
        number=70,
    )
    url_expansion_opt_out: bool = proto.Field(
        proto.BOOL,
        number=72,
        optional=True,
    )
    bidding_strategy: str = proto.Field(
        proto.STRING,
        number=67,
        oneof='campaign_bidding_strategy',
    )
    manual_cpa: bidding.ManualCpa = proto.Field(
        proto.MESSAGE,
        number=74,
        oneof='campaign_bidding_strategy',
        message=bidding.ManualCpa,
    )
    manual_cpc: bidding.ManualCpc = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof='campaign_bidding_strategy',
        message=bidding.ManualCpc,
    )
    manual_cpm: bidding.ManualCpm = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof='campaign_bidding_strategy',
        message=bidding.ManualCpm,
    )
    maximize_conversions: bidding.MaximizeConversions = proto.Field(
        proto.MESSAGE,
        number=30,
        oneof='campaign_bidding_strategy',
        message=bidding.MaximizeConversions,
    )
    maximize_conversion_value: bidding.MaximizeConversionValue = proto.Field(
        proto.MESSAGE,
        number=31,
        oneof='campaign_bidding_strategy',
        message=bidding.MaximizeConversionValue,
    )
    target_cpa: bidding.TargetCpa = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof='campaign_bidding_strategy',
        message=bidding.TargetCpa,
    )
    target_impression_share: bidding.TargetImpressionShare = proto.Field(
        proto.MESSAGE,
        number=48,
        oneof='campaign_bidding_strategy',
        message=bidding.TargetImpressionShare,
    )
    target_roas: bidding.TargetRoas = proto.Field(
        proto.MESSAGE,
        number=29,
        oneof='campaign_bidding_strategy',
        message=bidding.TargetRoas,
    )
    target_spend: bidding.TargetSpend = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof='campaign_bidding_strategy',
        message=bidding.TargetSpend,
    )
    percent_cpc: bidding.PercentCpc = proto.Field(
        proto.MESSAGE,
        number=34,
        oneof='campaign_bidding_strategy',
        message=bidding.PercentCpc,
    )
    target_cpm: bidding.TargetCpm = proto.Field(
        proto.MESSAGE,
        number=41,
        oneof='campaign_bidding_strategy',
        message=bidding.TargetCpm,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
