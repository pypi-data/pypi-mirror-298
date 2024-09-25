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

from google.ads.searchads360.v0.common.types import value
from google.ads.searchads360.v0.enums.types import interaction_event_type
from google.ads.searchads360.v0.enums.types import quality_score_bucket


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Metrics',
    },
)


class Metrics(proto.Message):
    r"""Metrics data.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        absolute_top_impression_percentage (float):
            Search absolute top impression share is the
            percentage of your Search ad impressions that
            are shown in the most prominent Search position.

            This field is a member of `oneof`_ ``_absolute_top_impression_percentage``.
        all_conversions_from_interactions_rate (float):
            All conversions from interactions (as oppose
            to view through conversions) divided by the
            number of ad interactions.

            This field is a member of `oneof`_ ``_all_conversions_from_interactions_rate``.
        all_conversions_value (float):
            The value of all conversions.

            This field is a member of `oneof`_ ``_all_conversions_value``.
        all_conversions_value_by_conversion_date (float):
            The value of all conversions. When this column is selected
            with date, the values in date column means the conversion
            date. Details for the by_conversion_date columns are
            available at
            https://support.google.com/sa360/answer/9250611.
        all_conversions (float):
            The total number of conversions. This includes all
            conversions regardless of the value of
            include_in_conversions_metric.

            This field is a member of `oneof`_ ``_all_conversions``.
        all_conversions_by_conversion_date (float):
            The total number of conversions. This includes all
            conversions regardless of the value of
            include_in_conversions_metric. When this column is selected
            with date, the values in date column means the conversion
            date. Details for the by_conversion_date columns are
            available at
            https://support.google.com/sa360/answer/9250611.
        all_conversions_value_per_cost (float):
            The value of all conversions divided by the
            total cost of ad interactions (such as clicks
            for text ads or views for video ads).

            This field is a member of `oneof`_ ``_all_conversions_value_per_cost``.
        all_conversions_from_click_to_call (float):
            The number of times people clicked the "Call"
            button to call a store during or after clicking
            an ad. This number doesn't include whether or
            not calls were connected, or the duration of any
            calls.

            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_click_to_call``.
        all_conversions_from_directions (float):
            The number of times people clicked a "Get
            directions" button to navigate to a store after
            clicking an ad.

            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_directions``.
        all_conversions_from_interactions_value_per_interaction (float):
            The value of all conversions from
            interactions divided by the total number of
            interactions.

            This field is a member of `oneof`_ ``_all_conversions_from_interactions_value_per_interaction``.
        all_conversions_from_menu (float):
            The number of times people clicked a link to
            view a store's menu after clicking an ad.

            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_menu``.
        all_conversions_from_order (float):
            The number of times people placed an order at
            a store after clicking an ad.
            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_order``.
        all_conversions_from_other_engagement (float):
            The number of other conversions (for example,
            posting a review or saving a location for a
            store) that occurred after people clicked an ad.

            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_other_engagement``.
        all_conversions_from_store_visit (float):
            Estimated number of times people visited a
            store after clicking an ad.
            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_store_visit``.
        visits (float):
            Clicks that Search Ads 360 has successfully
            recorded and forwarded to an advertiser's
            landing page.

            This field is a member of `oneof`_ ``_visits``.
        all_conversions_from_store_website (float):
            The number of times that people were taken to
            a store's URL after clicking an ad.

            This metric applies to feed items only.

            This field is a member of `oneof`_ ``_all_conversions_from_store_website``.
        average_cost (float):
            The average amount you pay per interaction.
            This amount is the total cost of your ads
            divided by the total number of interactions.

            This field is a member of `oneof`_ ``_average_cost``.
        average_cpc (float):
            The total cost of all clicks divided by the total number of
            clicks received. This metric is a monetary value and
            returned in the customer's currency by default. See the
            metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_average_cpc``.
        average_cpm (float):
            Average cost-per-thousand impressions (CPM). This metric is
            a monetary value and returned in the customer's currency by
            default. See the metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_average_cpm``.
        clicks (int):
            The number of clicks.

            This field is a member of `oneof`_ ``_clicks``.
        content_budget_lost_impression_share (float):
            The estimated percent of times that your ad
            was eligible to show on the Display Network but
            didn't because your budget was too low. Note:
            Content budget lost impression share is reported
            in the range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.

            This field is a member of `oneof`_ ``_content_budget_lost_impression_share``.
        content_impression_share (float):
            The impressions you've received on the
            Display Network divided by the estimated number
            of impressions you were eligible to receive.
            Note: Content impression share is reported in
            the range of 0.1 to 1. Any value below 0.1 is
            reported as 0.0999.

            This field is a member of `oneof`_ ``_content_impression_share``.
        conversion_custom_metrics (MutableSequence[google.ads.searchads360.v0.common.types.Value]):
            The conversion custom metrics.
        content_rank_lost_impression_share (float):
            The estimated percentage of impressions on
            the Display Network that your ads didn't receive
            due to poor Ad Rank. Note: Content rank lost
            impression share is reported in the range of 0
            to 0.9. Any value above 0.9 is reported as
            0.9001.

            This field is a member of `oneof`_ ``_content_rank_lost_impression_share``.
        conversions_from_interactions_rate (float):
            Average biddable conversions (from
            interaction) per conversion eligible
            interaction. Shows how often, on average, an ad
            interaction leads to a biddable conversion.

            This field is a member of `oneof`_ ``_conversions_from_interactions_rate``.
        client_account_conversions_value (float):
            The value of client account conversions. This only includes
            conversion actions which
            include_in_client_account_conversions_metric attribute is
            set to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.

            This field is a member of `oneof`_ ``_client_account_conversions_value``.
        conversions_value_by_conversion_date (float):
            The sum of biddable conversions value by
            conversion date. When this column is selected
            with date, the values in date column means the
            conversion date.
        conversions_value_per_cost (float):
            The value of biddable conversion divided by
            the total cost of conversion eligible
            interactions.

            This field is a member of `oneof`_ ``_conversions_value_per_cost``.
        conversions_from_interactions_value_per_interaction (float):
            The value of conversions from interactions divided by the
            number of ad interactions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.

            This field is a member of `oneof`_ ``_conversions_from_interactions_value_per_interaction``.
        client_account_conversions (float):
            The number of client account conversions. This only includes
            conversion actions which
            include_in_client_account_conversions_metric attribute is
            set to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.

            This field is a member of `oneof`_ ``_client_account_conversions``.
        conversions_by_conversion_date (float):
            The sum of conversions by conversion date for
            biddable conversion types. Can be fractional due
            to attribution modeling. When this column is
            selected with date, the values in date column
            means the conversion date.
        cost_micros (int):
            The sum of your cost-per-click (CPC) and cost-per-thousand
            impressions (CPM) costs during this period. This metric is a
            monetary value and returned in the customer's currency by
            default. See the metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_cost_micros``.
        cost_per_all_conversions (float):
            The cost of ad interactions divided by all
            conversions.

            This field is a member of `oneof`_ ``_cost_per_all_conversions``.
        cost_per_conversion (float):
            Average conversion eligible cost per biddable
            conversion.

            This field is a member of `oneof`_ ``_cost_per_conversion``.
        cost_per_current_model_attributed_conversion (float):
            The cost of ad interactions divided by current model
            attributed conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.

            This field is a member of `oneof`_ ``_cost_per_current_model_attributed_conversion``.
        cross_device_conversions (float):
            Conversions from when a customer clicks on an ad on one
            device, then converts on a different device or browser.
            Cross-device conversions are already included in
            all_conversions.

            This field is a member of `oneof`_ ``_cross_device_conversions``.
        cross_device_conversions_value (float):
            The sum of the value of cross-device
            conversions.

            This field is a member of `oneof`_ ``_cross_device_conversions_value``.
        ctr (float):
            The number of clicks your ad receives
            (Clicks) divided by the number of times your ad
            is shown (Impressions).

            This field is a member of `oneof`_ ``_ctr``.
        conversions (float):
            The number of conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.

            This field is a member of `oneof`_ ``_conversions``.
        conversions_value (float):
            The sum of conversion values for the
            conversions included in the "conversions" field.
            This metric is useful only if you entered a
            value for your conversion actions.

            This field is a member of `oneof`_ ``_conversions_value``.
        historical_creative_quality_score (google.ads.searchads360.v0.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The creative historical quality score.
        average_quality_score (float):
            The average quality score.

            This field is a member of `oneof`_ ``_average_quality_score``.
        historical_landing_page_quality_score (google.ads.searchads360.v0.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The quality of historical landing page
            experience.
        historical_quality_score (int):
            The historical quality score.

            This field is a member of `oneof`_ ``_historical_quality_score``.
        historical_search_predicted_ctr (google.ads.searchads360.v0.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The historical search predicted click through
            rate (CTR).
        impressions (int):
            Count of how often your ad has appeared on a
            search results page or website on the Google
            Network.

            This field is a member of `oneof`_ ``_impressions``.
        interaction_rate (float):
            How often people interact with your ad after
            it is shown to them. This is the number of
            interactions divided by the number of times your
            ad is shown.

            This field is a member of `oneof`_ ``_interaction_rate``.
        interactions (int):
            The number of interactions.
            An interaction is the main user action
            associated with an ad format-clicks for text and
            shopping ads, views for video ads, and so on.

            This field is a member of `oneof`_ ``_interactions``.
        interaction_event_types (MutableSequence[google.ads.searchads360.v0.enums.types.InteractionEventTypeEnum.InteractionEventType]):
            The types of payable and free interactions.
        invalid_click_rate (float):
            The percentage of clicks filtered out of your
            total number of clicks (filtered + non-filtered
            clicks) during the reporting period.

            This field is a member of `oneof`_ ``_invalid_click_rate``.
        invalid_clicks (int):
            Number of clicks Google considers
            illegitimate and doesn't charge you for.

            This field is a member of `oneof`_ ``_invalid_clicks``.
        mobile_friendly_clicks_percentage (float):
            The percentage of mobile clicks that go to a
            mobile-friendly page.

            This field is a member of `oneof`_ ``_mobile_friendly_clicks_percentage``.
        raw_event_conversion_metrics (MutableSequence[google.ads.searchads360.v0.common.types.Value]):
            The raw event conversion metrics.
        search_absolute_top_impression_share (float):
            The percentage of the customer's Shopping or
            Search ad impressions that are shown in the most
            prominent Shopping position. See
            https://support.google.com/sa360/answer/9566729
            for details. Any value below 0.1 is reported as
            0.0999.

            This field is a member of `oneof`_ ``_search_absolute_top_impression_share``.
        search_budget_lost_absolute_top_impression_share (float):
            The number estimating how often your ad
            wasn't the very first ad among the top ads in
            the search results due to a low budget. Note:
            Search budget lost absolute top impression share
            is reported in the range of 0 to 0.9. Any value
            above 0.9 is reported as 0.9001.

            This field is a member of `oneof`_ ``_search_budget_lost_absolute_top_impression_share``.
        search_budget_lost_impression_share (float):
            The estimated percent of times that your ad
            was eligible to show on the Search Network but
            didn't because your budget was too low. Note:
            Search budget lost impression share is reported
            in the range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.

            This field is a member of `oneof`_ ``_search_budget_lost_impression_share``.
        search_budget_lost_top_impression_share (float):
            The number estimating how often your ad
            didn't show adjacent to the top organic search
            results due to a low budget. Note: Search budget
            lost top impression share is reported in the
            range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.

            This field is a member of `oneof`_ ``_search_budget_lost_top_impression_share``.
        search_click_share (float):
            The number of clicks you've received on the
            Search Network divided by the estimated number
            of clicks you were eligible to receive. Note:
            Search click share is reported in the range of
            0.1 to 1. Any value below 0.1 is reported as
            0.0999.

            This field is a member of `oneof`_ ``_search_click_share``.
        search_exact_match_impression_share (float):
            The impressions you've received divided by
            the estimated number of impressions you were
            eligible to receive on the Search Network for
            search terms that matched your keywords exactly
            (or were close variants of your keyword),
            regardless of your keyword match types. Note:
            Search exact match impression share is reported
            in the range of 0.1 to 1. Any value below 0.1 is
            reported as 0.0999.

            This field is a member of `oneof`_ ``_search_exact_match_impression_share``.
        search_impression_share (float):
            The impressions you've received on the Search
            Network divided by the estimated number of
            impressions you were eligible to receive. Note:
            Search impression share is reported in the range
            of 0.1 to 1. Any value below 0.1 is reported as
            0.0999.

            This field is a member of `oneof`_ ``_search_impression_share``.
        search_rank_lost_absolute_top_impression_share (float):
            The number estimating how often your ad
            wasn't the very first ad among the top ads in
            the search results due to poor Ad Rank. Note:
            Search rank lost absolute top impression share
            is reported in the range of 0 to 0.9. Any value
            above 0.9 is reported as 0.9001.

            This field is a member of `oneof`_ ``_search_rank_lost_absolute_top_impression_share``.
        search_rank_lost_impression_share (float):
            The estimated percentage of impressions on
            the Search Network that your ads didn't receive
            due to poor Ad Rank. Note: Search rank lost
            impression share is reported in the range of 0
            to 0.9. Any value above 0.9 is reported as
            0.9001.

            This field is a member of `oneof`_ ``_search_rank_lost_impression_share``.
        search_rank_lost_top_impression_share (float):
            The number estimating how often your ad
            didn't show adjacent to the top organic search
            results due to poor Ad Rank. Note: Search rank
            lost top impression share is reported in the
            range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.

            This field is a member of `oneof`_ ``_search_rank_lost_top_impression_share``.
        search_top_impression_share (float):
            The impressions you've received among the top
            ads compared to the estimated number of
            impressions you were eligible to receive among
            the top ads. Note: Search top impression share
            is reported in the range of 0.1 to 1. Any value
            below 0.1 is reported as 0.0999.

            Top ads are generally above the top organic
            results, although they may show below the top
            organic results on certain queries.

            This field is a member of `oneof`_ ``_search_top_impression_share``.
        top_impression_percentage (float):
            The percent of your ad impressions that are
            shown adjacent to the top organic search
            results.

            This field is a member of `oneof`_ ``_top_impression_percentage``.
        value_per_all_conversions (float):
            The value of all conversions divided by the
            number of all conversions.

            This field is a member of `oneof`_ ``_value_per_all_conversions``.
        value_per_all_conversions_by_conversion_date (float):
            The value of all conversions divided by the number of all
            conversions. When this column is selected with date, the
            values in date column means the conversion date. Details for
            the by_conversion_date columns are available at
            https://support.google.com/sa360/answer/9250611.

            This field is a member of `oneof`_ ``_value_per_all_conversions_by_conversion_date``.
        value_per_conversion (float):
            The value of biddable conversion divided by
            the number of biddable conversions. Shows how
            much, on average, each of the biddable
            conversions is worth.

            This field is a member of `oneof`_ ``_value_per_conversion``.
        value_per_conversions_by_conversion_date (float):
            Biddable conversions value by conversion date
            divided by biddable conversions by conversion
            date. Shows how much, on average, each of the
            biddable conversions is worth (by conversion
            date). When this column is selected with date,
            the values in date column means the conversion
            date.

            This field is a member of `oneof`_ ``_value_per_conversions_by_conversion_date``.
        client_account_view_through_conversions (int):
            The total number of view-through conversions.
            These happen when a customer sees an image or
            rich media ad, then later completes a conversion
            on your site without interacting with (for
            example, clicking on) another ad.

            This field is a member of `oneof`_ ``_client_account_view_through_conversions``.
        client_account_cross_sell_cost_of_goods_sold_micros (int):
            Client account cross-sell cost of goods sold (COGS) is the
            total cost of products sold as a result of advertising a
            different product. How it works: You report conversions with
            cart data for completed purchases on your website. If the ad
            that was interacted with before the purchase has an
            associated product (see Shopping Ads) then this product is
            considered the advertised product. Any product included in
            the order the customer places is a sold product. If these
            products don't match then this is considered cross-sell.
            Cross-sell cost of goods sold is the total cost of the
            products sold that weren't advertised. Example: Someone
            clicked on a Shopping ad for a hat then bought the same hat
            and a shirt. The hat has a cost of goods sold value of $3,
            the shirt has a cost of goods sold value of $5. The
            cross-sell cost of goods sold for this order is $5. This
            metric is only available if you report conversions with cart
            data. This metric is a monetary value and returned in the
            customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_cross_sell_cost_of_goods_sold_micros``.
        cross_sell_cost_of_goods_sold_micros (int):
            Cross-sell cost of goods sold (COGS) is the total cost of
            products sold as a result of advertising a different
            product. How it works: You report conversions with cart data
            for completed purchases on your website. If the ad that was
            interacted with before the purchase has an associated
            product (see Shopping Ads) then this product is considered
            the advertised product. Any product included in the order
            the customer places is a sold product. If these products
            don't match then this is considered cross-sell. Cross-sell
            cost of goods sold is the total cost of the products sold
            that weren't advertised. Example: Someone clicked on a
            Shopping ad for a hat then bought the same hat and a shirt.
            The hat has a cost of goods sold value of $3, the shirt has
            a cost of goods sold value of $5. The cross-sell cost of
            goods sold for this order is $5. This metric is only
            available if you report conversions with cart data. This
            metric is a monetary value and returned in the customer's
            currency by default. See the metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_cross_sell_cost_of_goods_sold_micros``.
        client_account_cross_sell_gross_profit_micros (int):
            Client account cross-sell gross profit is the profit you
            made from products sold as a result of advertising a
            different product, minus cost of goods sold (COGS). How it
            works: You report conversions with cart data for completed
            purchases on your website. If the ad that was interacted
            with before the purchase has an associated product (see
            Shopping Ads) then this product is considered the advertised
            product. Any product included in the purchase is a sold
            product. If these products don't match then this is
            considered cross-sell. Cross-sell gross profit is the
            revenue you made from cross-sell attributed to your ads
            minus the cost of the goods sold. Example: Someone clicked
            on a Shopping ad for a hat then bought the same hat and a
            shirt. The shirt is priced $20 and has a cost of goods sold
            value of $5. The cross-sell gross profit of this order is
            $15 = $20 - $5. This metric is only available if you report
            conversions with cart data. This metric is a monetary value
            and returned in the customer's currency by default. See the
            metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_cross_sell_gross_profit_micros``.
        cross_sell_gross_profit_micros (int):
            Cross-sell gross profit is the profit you made from products
            sold as a result of advertising a different product, minus
            cost of goods sold (COGS). How it works: You report
            conversions with cart data for completed purchases on your
            website. If the ad that was interacted with before the
            purchase has an associated product (see Shopping Ads) then
            this product is considered the advertised product. Any
            product included in the purchase is a sold product. If these
            products don't match then this is considered cross-sell.
            Cross-sell gross profit is the revenue you made from
            cross-sell attributed to your ads minus the cost of the
            goods sold. Example: Someone clicked on a Shopping ad for a
            hat then bought the same hat and a shirt. The shirt is
            priced $20 and has a cost of goods sold value of $5. The
            cross-sell gross profit of this order is $15 = $20 - $5.
            This metric is only available if you report conversions with
            cart data. This metric is a monetary value and returned in
            the customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_cross_sell_gross_profit_micros``.
        client_account_cross_sell_revenue_micros (int):
            Client account cross-sell revenue is the total amount you
            made from products sold as a result of advertising a
            different product. How it works: You report conversions with
            cart data for completed purchases on your website. If the ad
            that was interacted with before the purchase has an
            associated product (see Shopping Ads) then this product is
            considered the advertised product. Any product included in
            the order the customer places is a sold product. If these
            products don't match then this is considered cross-sell.
            Cross-sell revenue is the total value you made from
            cross-sell attributed to your ads. Example: Someone clicked
            on a Shopping ad for a hat then bought the same hat and a
            shirt. The hat is priced $10 and the shirt is priced $20.
            The cross-sell revenue of this order is $20. This metric is
            only available if you report conversions with cart data.
            This metric is a monetary value and returned in the
            customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_cross_sell_revenue_micros``.
        cross_sell_revenue_micros (int):
            Cross-sell revenue is the total amount you made from
            products sold as a result of advertising a different
            product. How it works: You report conversions with cart data
            for completed purchases on your website. If the ad that was
            interacted with before the purchase has an associated
            product (see Shopping Ads) then this product is considered
            the advertised product. Any product included in the order
            the customer places is a sold product. If these products
            don't match then this is considered cross-sell. Cross-sell
            revenue is the total value you made from cross-sell
            attributed to your ads. Example: Someone clicked on a
            Shopping ad for a hat then bought the same hat and a shirt.
            The hat is priced $10 and the shirt is priced $20. The
            cross-sell revenue of this order is $20. This metric is only
            available if you report conversions with cart data. This
            metric is a monetary value and returned in the customer's
            currency by default. See the metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_cross_sell_revenue_micros``.
        client_account_cross_sell_units_sold (float):
            Client account cross-sell units sold is
            the total number of products sold as a result of
            advertising a different product.
            How it works: You report conversions with cart
            data for completed purchases on your website. If
            the ad that was interacted with before the
            purchase has an associated product (see Shopping
            Ads) then this product is considered the
            advertised product. Any product included in the
            order the customer places is a sold product. If
            these products don't match then this is
            considered cross-sell. Cross-sell units sold is
            the total number of cross-sold products from all
            orders attributed to your ads. Example: Someone
            clicked on a Shopping ad for a hat then bought
            the same hat, a shirt and a jacket. The
            cross-sell units sold in this order is 2. This
            metric is only available if you report
            conversions with cart data.

            This field is a member of `oneof`_ ``_client_account_cross_sell_units_sold``.
        cross_sell_units_sold (float):
            Cross-sell units sold is the total number of
            products sold as a result of advertising a
            different product. How it works: You report
            conversions with cart data for completed
            purchases on your website. If the ad that was
            interacted with before the purchase has an
            associated product (see Shopping Ads) then this
            product is considered the advertised product.
            Any product included in the order the customer
            places is a sold product. If these products
            don't match then this is considered cross-sell.
            Cross-sell units sold is the total number of
            cross-sold products from all orders attributed
            to your ads. Example: Someone clicked on a
            Shopping ad for a hat then bought the same hat,
            a shirt and a jacket. The cross-sell units sold
            in this order is 2. This metric is only
            available if you report conversions with cart
            data.

            This field is a member of `oneof`_ ``_cross_sell_units_sold``.
        client_account_lead_cost_of_goods_sold_micros (int):
            Client account lead cost of goods sold (COGS) is the total
            cost of products sold as a result of advertising the same
            product. How it works: You report conversions with cart data
            for completed purchases on your website. If the ad that was
            interacted with has an associated product (see Shopping Ads)
            then this product is considered the advertised product. Any
            product included in the order the customer places is a sold
            product. If the advertised and sold products match, then the
            cost of these goods is counted under lead cost of goods
            sold. Example: Someone clicked on a Shopping ad for a hat
            then bought the same hat and a shirt. The hat has a cost of
            goods sold value of $3, the shirt has a cost of goods sold
            value of $5. The lead cost of goods sold for this order is
            $3. This metric is only available if you report conversions
            with cart data. This metric is a monetary value and returned
            in the customer's currency by default. See the
            metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_lead_cost_of_goods_sold_micros``.
        lead_cost_of_goods_sold_micros (int):
            Lead cost of goods sold (COGS) is the total cost of products
            sold as a result of advertising the same product. How it
            works: You report conversions with cart data for completed
            purchases on your website. If the ad that was interacted
            with has an associated product (see Shopping Ads) then this
            product is considered the advertised product. Any product
            included in the order the customer places is a sold product.
            If the advertised and sold products match, then the cost of
            these goods is counted under lead cost of goods sold.
            Example: Someone clicked on a Shopping ad for a hat then
            bought the same hat and a shirt. The hat has a cost of goods
            sold value of $3, the shirt has a cost of goods sold value
            of $5. The lead cost of goods sold for this order is $3.
            This metric is only available if you report conversions with
            cart data. This metric is a monetary value and returned in
            the customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_lead_cost_of_goods_sold_micros``.
        client_account_lead_gross_profit_micros (int):
            Client account lead gross profit is the profit you made from
            products sold as a result of advertising the same product,
            minus cost of goods sold (COGS). How it works: You report
            conversions with cart data for completed purchases on your
            website. If the ad that was interacted with before the
            purchase has an associated product (see Shopping Ads) then
            this product is considered the advertised product. Any
            product included in the order the customer places is a sold
            product. If the advertised and sold products match, then the
            revenue you made from these sales minus the cost of goods
            sold is your lead gross profit. Example: Someone clicked on
            a Shopping ad for a hat then bought the same hat and a
            shirt. The hat is priced $10 and has a cost of goods sold
            value of $3. The lead gross profit of this order is $7 = $10
            - $3. This metric is only available if you report
            conversions with cart data. This metric is a monetary value
            and returned in the customer's currency by default. See the
            metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_lead_gross_profit_micros``.
        lead_gross_profit_micros (int):
            Lead gross profit is the profit you made from products sold
            as a result of advertising the same product, minus cost of
            goods sold (COGS). How it works: You report conversions with
            cart data for completed purchases on your website. If the ad
            that was interacted with before the purchase has an
            associated product (see Shopping Ads) then this product is
            considered the advertised product. Any product included in
            the order the customer places is a sold product. If the
            advertised and sold products match, then the revenue you
            made from these sales minus the cost of goods sold is your
            lead gross profit. Example: Someone clicked on a Shopping ad
            for a hat then bought the same hat and a shirt. The hat is
            priced $10 and has a cost of goods sold value of $3. The
            lead gross profit of this order is $7 = $10 - $3. This
            metric is only available if you report conversions with cart
            data. This metric is a monetary value and returned in the
            customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_lead_gross_profit_micros``.
        client_account_lead_revenue_micros (int):
            Client account lead revenue is the total amount you made
            from products sold as a result of advertising the same
            product. How it works: You report conversions with cart data
            for completed purchases on your website. If the ad that was
            interacted with before the purchase has an associated
            product (see Shopping Ads) then this product is considered
            the advertised product. Any product included in the order
            the customer places is a sold product. If the advertised and
            sold products match, then the total value you made from the
            sales of these products is shown under lead revenue.
            Example: Someone clicked on a Shopping ad for a hat then
            bought the same hat and a shirt. The hat is priced $10 and
            the shirt is priced $20. The lead revenue of this order is
            $10. This metric is only available if you report conversions
            with cart data. This metric is a monetary value and returned
            in the customer's currency by default. See the
            metrics_currency parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_client_account_lead_revenue_micros``.
        lead_revenue_micros (int):
            Lead revenue is the total amount you made from products sold
            as a result of advertising the same product. How it works:
            You report conversions with cart data for completed
            purchases on your website. If the ad that was interacted
            with before the purchase has an associated product (see
            Shopping Ads) then this product is considered the advertised
            product. Any product included in the order the customer
            places is a sold product. If the advertised and sold
            products match, then the total value you made from the sales
            of these products is shown under lead revenue. Example:
            Someone clicked on a Shopping ad for a hat then bought the
            same hat and a shirt. The hat is priced $10 and the shirt is
            priced $20. The lead revenue of this order is $10. This
            metric is only available if you report conversions with cart
            data. This metric is a monetary value and returned in the
            customer's currency by default. See the metrics_currency
            parameter at
            https://developers.google.com/search-ads/reporting/query/query-structure#parameters_clause

            This field is a member of `oneof`_ ``_lead_revenue_micros``.
        client_account_lead_units_sold (float):
            Client account lead units sold is the total
            number of products sold as a result of
            advertising the same product. How it works: You
            report conversions with cart data for completed
            purchases on your website. If the ad that was
            interacted with before the purchase has an
            associated product (see Shopping Ads) then this
            product is considered the advertised product.
            Any product included in the order the customer
            places is a sold product. If the advertised and
            sold products match, then the total number of
            these products sold is shown under lead units
            sold. Example: Someone clicked on a Shopping ad
            for a hat then bought the same hat, a shirt and
            a jacket. The lead units sold in this order is
            1. This metric is only available if you report
            conversions with cart data.

            This field is a member of `oneof`_ ``_client_account_lead_units_sold``.
        lead_units_sold (float):
            Lead units sold is the total number of
            products sold as a result of advertising the
            same product. How it works: You report
            conversions with cart data for completed
            purchases on your website. If the ad that was
            interacted with before the purchase has an
            associated product (see Shopping Ads) then this
            product is considered the advertised product.
            Any product included in the order the customer
            places is a sold product. If the advertised and
            sold products match, then the total number of
            these products sold is shown under lead units
            sold. Example: Someone clicked on a Shopping ad
            for a hat then bought the same hat, a shirt and
            a jacket. The lead units sold in this order is
            1. This metric is only available if you report
            conversions with cart data.

            This field is a member of `oneof`_ ``_lead_units_sold``.
    """

    absolute_top_impression_percentage: float = proto.Field(
        proto.DOUBLE,
        number=183,
        optional=True,
    )
    all_conversions_from_interactions_rate: float = proto.Field(
        proto.DOUBLE,
        number=191,
        optional=True,
    )
    all_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=192,
        optional=True,
    )
    all_conversions_value_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=240,
    )
    all_conversions: float = proto.Field(
        proto.DOUBLE,
        number=193,
        optional=True,
    )
    all_conversions_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=241,
    )
    all_conversions_value_per_cost: float = proto.Field(
        proto.DOUBLE,
        number=194,
        optional=True,
    )
    all_conversions_from_click_to_call: float = proto.Field(
        proto.DOUBLE,
        number=195,
        optional=True,
    )
    all_conversions_from_directions: float = proto.Field(
        proto.DOUBLE,
        number=196,
        optional=True,
    )
    all_conversions_from_interactions_value_per_interaction: float = proto.Field(
        proto.DOUBLE,
        number=197,
        optional=True,
    )
    all_conversions_from_menu: float = proto.Field(
        proto.DOUBLE,
        number=198,
        optional=True,
    )
    all_conversions_from_order: float = proto.Field(
        proto.DOUBLE,
        number=199,
        optional=True,
    )
    all_conversions_from_other_engagement: float = proto.Field(
        proto.DOUBLE,
        number=200,
        optional=True,
    )
    all_conversions_from_store_visit: float = proto.Field(
        proto.DOUBLE,
        number=201,
        optional=True,
    )
    visits: float = proto.Field(
        proto.DOUBLE,
        number=289,
        optional=True,
    )
    all_conversions_from_store_website: float = proto.Field(
        proto.DOUBLE,
        number=202,
        optional=True,
    )
    average_cost: float = proto.Field(
        proto.DOUBLE,
        number=203,
        optional=True,
    )
    average_cpc: float = proto.Field(
        proto.DOUBLE,
        number=317,
        optional=True,
    )
    average_cpm: float = proto.Field(
        proto.DOUBLE,
        number=318,
        optional=True,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=131,
        optional=True,
    )
    content_budget_lost_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=159,
        optional=True,
    )
    content_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=160,
        optional=True,
    )
    conversion_custom_metrics: MutableSequence[value.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=336,
        message=value.Value,
    )
    content_rank_lost_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=163,
        optional=True,
    )
    conversions_from_interactions_rate: float = proto.Field(
        proto.DOUBLE,
        number=284,
        optional=True,
    )
    client_account_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=165,
        optional=True,
    )
    conversions_value_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=283,
    )
    conversions_value_per_cost: float = proto.Field(
        proto.DOUBLE,
        number=288,
        optional=True,
    )
    conversions_from_interactions_value_per_interaction: float = proto.Field(
        proto.DOUBLE,
        number=167,
        optional=True,
    )
    client_account_conversions: float = proto.Field(
        proto.DOUBLE,
        number=168,
        optional=True,
    )
    conversions_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=282,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=316,
        optional=True,
    )
    cost_per_all_conversions: float = proto.Field(
        proto.DOUBLE,
        number=170,
        optional=True,
    )
    cost_per_conversion: float = proto.Field(
        proto.DOUBLE,
        number=286,
        optional=True,
    )
    cost_per_current_model_attributed_conversion: float = proto.Field(
        proto.DOUBLE,
        number=172,
        optional=True,
    )
    cross_device_conversions: float = proto.Field(
        proto.DOUBLE,
        number=173,
        optional=True,
    )
    cross_device_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=253,
        optional=True,
    )
    ctr: float = proto.Field(
        proto.DOUBLE,
        number=174,
        optional=True,
    )
    conversions: float = proto.Field(
        proto.DOUBLE,
        number=251,
        optional=True,
    )
    conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=252,
        optional=True,
    )
    historical_creative_quality_score: quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket = proto.Field(
        proto.ENUM,
        number=80,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    average_quality_score: float = proto.Field(
        proto.DOUBLE,
        number=364,
        optional=True,
    )
    historical_landing_page_quality_score: quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket = proto.Field(
        proto.ENUM,
        number=81,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    historical_quality_score: int = proto.Field(
        proto.INT64,
        number=216,
        optional=True,
    )
    historical_search_predicted_ctr: quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket = proto.Field(
        proto.ENUM,
        number=83,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=221,
        optional=True,
    )
    interaction_rate: float = proto.Field(
        proto.DOUBLE,
        number=222,
        optional=True,
    )
    interactions: int = proto.Field(
        proto.INT64,
        number=223,
        optional=True,
    )
    interaction_event_types: MutableSequence[interaction_event_type.InteractionEventTypeEnum.InteractionEventType] = proto.RepeatedField(
        proto.ENUM,
        number=100,
        enum=interaction_event_type.InteractionEventTypeEnum.InteractionEventType,
    )
    invalid_click_rate: float = proto.Field(
        proto.DOUBLE,
        number=224,
        optional=True,
    )
    invalid_clicks: int = proto.Field(
        proto.INT64,
        number=225,
        optional=True,
    )
    mobile_friendly_clicks_percentage: float = proto.Field(
        proto.DOUBLE,
        number=229,
        optional=True,
    )
    raw_event_conversion_metrics: MutableSequence[value.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=337,
        message=value.Value,
    )
    search_absolute_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=136,
        optional=True,
    )
    search_budget_lost_absolute_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=137,
        optional=True,
    )
    search_budget_lost_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=138,
        optional=True,
    )
    search_budget_lost_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=139,
        optional=True,
    )
    search_click_share: float = proto.Field(
        proto.DOUBLE,
        number=140,
        optional=True,
    )
    search_exact_match_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=141,
        optional=True,
    )
    search_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=142,
        optional=True,
    )
    search_rank_lost_absolute_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=143,
        optional=True,
    )
    search_rank_lost_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=144,
        optional=True,
    )
    search_rank_lost_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=145,
        optional=True,
    )
    search_top_impression_share: float = proto.Field(
        proto.DOUBLE,
        number=146,
        optional=True,
    )
    top_impression_percentage: float = proto.Field(
        proto.DOUBLE,
        number=148,
        optional=True,
    )
    value_per_all_conversions: float = proto.Field(
        proto.DOUBLE,
        number=150,
        optional=True,
    )
    value_per_all_conversions_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=244,
        optional=True,
    )
    value_per_conversion: float = proto.Field(
        proto.DOUBLE,
        number=287,
        optional=True,
    )
    value_per_conversions_by_conversion_date: float = proto.Field(
        proto.DOUBLE,
        number=285,
        optional=True,
    )
    client_account_view_through_conversions: int = proto.Field(
        proto.INT64,
        number=155,
        optional=True,
    )
    client_account_cross_sell_cost_of_goods_sold_micros: int = proto.Field(
        proto.INT64,
        number=321,
        optional=True,
    )
    cross_sell_cost_of_goods_sold_micros: int = proto.Field(
        proto.INT64,
        number=327,
        optional=True,
    )
    client_account_cross_sell_gross_profit_micros: int = proto.Field(
        proto.INT64,
        number=322,
        optional=True,
    )
    cross_sell_gross_profit_micros: int = proto.Field(
        proto.INT64,
        number=328,
        optional=True,
    )
    client_account_cross_sell_revenue_micros: int = proto.Field(
        proto.INT64,
        number=323,
        optional=True,
    )
    cross_sell_revenue_micros: int = proto.Field(
        proto.INT64,
        number=329,
        optional=True,
    )
    client_account_cross_sell_units_sold: float = proto.Field(
        proto.DOUBLE,
        number=307,
        optional=True,
    )
    cross_sell_units_sold: float = proto.Field(
        proto.DOUBLE,
        number=330,
        optional=True,
    )
    client_account_lead_cost_of_goods_sold_micros: int = proto.Field(
        proto.INT64,
        number=324,
        optional=True,
    )
    lead_cost_of_goods_sold_micros: int = proto.Field(
        proto.INT64,
        number=332,
        optional=True,
    )
    client_account_lead_gross_profit_micros: int = proto.Field(
        proto.INT64,
        number=325,
        optional=True,
    )
    lead_gross_profit_micros: int = proto.Field(
        proto.INT64,
        number=333,
        optional=True,
    )
    client_account_lead_revenue_micros: int = proto.Field(
        proto.INT64,
        number=326,
        optional=True,
    )
    lead_revenue_micros: int = proto.Field(
        proto.INT64,
        number=334,
        optional=True,
    )
    client_account_lead_units_sold: float = proto.Field(
        proto.DOUBLE,
        number=311,
        optional=True,
    )
    lead_units_sold: float = proto.Field(
        proto.DOUBLE,
        number=335,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
