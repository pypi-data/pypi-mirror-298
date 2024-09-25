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
from collections import OrderedDict
import os
import re
from typing import Callable, Dict, Mapping, MutableMapping, MutableSequence, Optional, Iterable, Sequence, Tuple, Type, Union, cast

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials             # type: ignore
from google.auth.transport import mtls                            # type: ignore
from google.auth.transport.grpc import SslCredentials             # type: ignore
from google.auth.exceptions import MutualTLSChannelError          # type: ignore
from google.oauth2 import service_account                         # type: ignore


from google.ads.searchads360.v0 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.ads.searchads360.v0.services.services.search_ads360_service import pagers
from google.ads.searchads360.v0.services.types import search_ads360_service
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import SearchAds360ServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import SearchAds360ServiceGrpcTransport


class SearchAds360ServiceClientMeta(type):
    """Metaclass for the SearchAds360Service client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[SearchAds360ServiceTransport]]
    _transport_registry['grpc'] = SearchAds360ServiceGrpcTransport

    def get_transport_class(cls,
            label: Optional[str] = None,
            ) -> Type[SearchAds360ServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class SearchAds360ServiceClient(metaclass=SearchAds360ServiceClientMeta):
    """Service to fetch data and metrics across resources."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "searchads360.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SearchAds360ServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            SearchAds360ServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SearchAds360ServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            SearchAds360ServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    def __enter__(self) -> "SearchAds360ServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    @staticmethod
    def accessible_bidding_strategy_path(customer_id: str,bidding_strategy_id: str,) -> str:
        """Returns a fully-qualified accessible_bidding_strategy string."""
        return "customers/{customer_id}/accessibleBiddingStrategies/{bidding_strategy_id}".format(customer_id=customer_id, bidding_strategy_id=bidding_strategy_id, )

    @staticmethod
    def parse_accessible_bidding_strategy_path(path: str) -> Dict[str,str]:
        """Parses a accessible_bidding_strategy path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/accessibleBiddingStrategies/(?P<bidding_strategy_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_path(customer_id: str,ad_id: str,) -> str:
        """Returns a fully-qualified ad string."""
        return "customers/{customer_id}/ads/{ad_id}".format(customer_id=customer_id, ad_id=ad_id, )

    @staticmethod
    def parse_ad_path(path: str) -> Dict[str,str]:
        """Parses a ad path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/ads/(?P<ad_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_path(customer_id: str,ad_group_id: str,) -> str:
        """Returns a fully-qualified ad_group string."""
        return "customers/{customer_id}/adGroups/{ad_group_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, )

    @staticmethod
    def parse_ad_group_path(path: str) -> Dict[str,str]:
        """Parses a ad_group path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroups/(?P<ad_group_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_path(customer_id: str,ad_group_id: str,ad_id: str,) -> str:
        """Returns a fully-qualified ad_group_ad string."""
        return "customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, ad_id=ad_id, )

    @staticmethod
    def parse_ad_group_ad_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_ad path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupAds/(?P<ad_group_id>.+?)~(?P<ad_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_label_path(customer_id: str,ad_group_id: str,ad_id: str,entity_id: str,) -> str:
        """Returns a fully-qualified ad_group_ad_label string."""
        return "customers/{customer_id}/adGroupAdLabels/{ad_group_id}~{ad_id}~{entity_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, ad_id=ad_id, entity_id=entity_id, )

    @staticmethod
    def parse_ad_group_ad_label_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_ad_label path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupAdLabels/(?P<ad_group_id>.+?)~(?P<ad_id>.+?)~(?P<entity_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_asset_path(customer_id: str,ad_group_id: str,asset_id: str,field_type: str,) -> str:
        """Returns a fully-qualified ad_group_asset string."""
        return "customers/{customer_id}/adGroupAssets/{ad_group_id}~{asset_id}~{field_type}".format(customer_id=customer_id, ad_group_id=ad_group_id, asset_id=asset_id, field_type=field_type, )

    @staticmethod
    def parse_ad_group_asset_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupAssets/(?P<ad_group_id>.+?)~(?P<asset_id>.+?)~(?P<field_type>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_asset_set_path(customer_id: str,ad_group_id: str,asset_set_id: str,) -> str:
        """Returns a fully-qualified ad_group_asset_set string."""
        return "customers/{customer_id}/adGroupAssetSets/{ad_group_id}~{asset_set_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, asset_set_id=asset_set_id, )

    @staticmethod
    def parse_ad_group_asset_set_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_asset_set path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupAssetSets/(?P<ad_group_id>.+?)~(?P<asset_set_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_audience_view_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified ad_group_audience_view string."""
        return "customers/{customer_id}/adGroupAudienceViews/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_ad_group_audience_view_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_audience_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupAudienceViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_bid_modifier_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified ad_group_bid_modifier string."""
        return "customers/{customer_id}/adGroupBidModifiers/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_ad_group_bid_modifier_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_bid_modifier path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupBidModifiers/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified ad_group_criterion string."""
        return "customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_ad_group_criterion_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_criterion path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupCriteria/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_label_path(customer_id: str,ad_group_id: str,criterion_id: str,entity_id: str,) -> str:
        """Returns a fully-qualified ad_group_criterion_label string."""
        return "customers/{customer_id}/adGroupCriterionLabels/{ad_group_id}~{criterion_id}~{entity_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, entity_id=entity_id, )

    @staticmethod
    def parse_ad_group_criterion_label_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_criterion_label path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupCriterionLabels/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)~(?P<entity_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_label_path(customer_id: str,ad_group_id: str,entity_id: str,) -> str:
        """Returns a fully-qualified ad_group_label string."""
        return "customers/{customer_id}/adGroupLabels/{ad_group_id}~{entity_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, entity_id=entity_id, )

    @staticmethod
    def parse_ad_group_label_path(path: str) -> Dict[str,str]:
        """Parses a ad_group_label path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/adGroupLabels/(?P<ad_group_id>.+?)~(?P<entity_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def age_range_view_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified age_range_view string."""
        return "customers/{customer_id}/ageRangeViews/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_age_range_view_path(path: str) -> Dict[str,str]:
        """Parses a age_range_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/ageRangeViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_path(customer_id: str,asset_id: str,) -> str:
        """Returns a fully-qualified asset string."""
        return "customers/{customer_id}/assets/{asset_id}".format(customer_id=customer_id, asset_id=asset_id, )

    @staticmethod
    def parse_asset_path(path: str) -> Dict[str,str]:
        """Parses a asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assets/(?P<asset_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_group_path(customer_id: str,asset_group_id: str,) -> str:
        """Returns a fully-qualified asset_group string."""
        return "customers/{customer_id}/assetGroups/{asset_group_id}".format(customer_id=customer_id, asset_group_id=asset_group_id, )

    @staticmethod
    def parse_asset_group_path(path: str) -> Dict[str,str]:
        """Parses a asset_group path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetGroups/(?P<asset_group_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_group_asset_path(customer_id: str,asset_group_id: str,asset_id: str,field_type: str,) -> str:
        """Returns a fully-qualified asset_group_asset string."""
        return "customers/{customer_id}/assetGroupAssets/{asset_group_id}~{asset_id}~{field_type}".format(customer_id=customer_id, asset_group_id=asset_group_id, asset_id=asset_id, field_type=field_type, )

    @staticmethod
    def parse_asset_group_asset_path(path: str) -> Dict[str,str]:
        """Parses a asset_group_asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetGroupAssets/(?P<asset_group_id>.+?)~(?P<asset_id>.+?)~(?P<field_type>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_group_listing_group_filter_path(customer_id: str,asset_group_id: str,listing_group_filter_id: str,) -> str:
        """Returns a fully-qualified asset_group_listing_group_filter string."""
        return "customers/{customer_id}/assetGroupListingGroupFilters/{asset_group_id}~{listing_group_filter_id}".format(customer_id=customer_id, asset_group_id=asset_group_id, listing_group_filter_id=listing_group_filter_id, )

    @staticmethod
    def parse_asset_group_listing_group_filter_path(path: str) -> Dict[str,str]:
        """Parses a asset_group_listing_group_filter path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetGroupListingGroupFilters/(?P<asset_group_id>.+?)~(?P<listing_group_filter_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_group_signal_path(customer_id: str,asset_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified asset_group_signal string."""
        return "customers/{customer_id}/assetGroupSignals/{asset_group_id}~{criterion_id}".format(customer_id=customer_id, asset_group_id=asset_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_asset_group_signal_path(path: str) -> Dict[str,str]:
        """Parses a asset_group_signal path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetGroupSignals/(?P<asset_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_group_top_combination_view_path(customer_id: str,asset_group_id: str,asset_combination_category: str,) -> str:
        """Returns a fully-qualified asset_group_top_combination_view string."""
        return "customers/{customer_id}/assetGroupTopCombinationViews/{asset_group_id}~{asset_combination_category}".format(customer_id=customer_id, asset_group_id=asset_group_id, asset_combination_category=asset_combination_category, )

    @staticmethod
    def parse_asset_group_top_combination_view_path(path: str) -> Dict[str,str]:
        """Parses a asset_group_top_combination_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetGroupTopCombinationViews/(?P<asset_group_id>.+?)~(?P<asset_combination_category>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_set_path(customer_id: str,asset_set_id: str,) -> str:
        """Returns a fully-qualified asset_set string."""
        return "customers/{customer_id}/assetSets/{asset_set_id}".format(customer_id=customer_id, asset_set_id=asset_set_id, )

    @staticmethod
    def parse_asset_set_path(path: str) -> Dict[str,str]:
        """Parses a asset_set path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetSets/(?P<asset_set_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def asset_set_asset_path(customer_id: str,asset_set_id: str,asset_id: str,) -> str:
        """Returns a fully-qualified asset_set_asset string."""
        return "customers/{customer_id}/assetSetAssets/{asset_set_id}~{asset_id}".format(customer_id=customer_id, asset_set_id=asset_set_id, asset_id=asset_id, )

    @staticmethod
    def parse_asset_set_asset_path(path: str) -> Dict[str,str]:
        """Parses a asset_set_asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/assetSetAssets/(?P<asset_set_id>.+?)~(?P<asset_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def audience_path(customer_id: str,audience_id: str,) -> str:
        """Returns a fully-qualified audience string."""
        return "customers/{customer_id}/audiences/{audience_id}".format(customer_id=customer_id, audience_id=audience_id, )

    @staticmethod
    def parse_audience_path(path: str) -> Dict[str,str]:
        """Parses a audience path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/audiences/(?P<audience_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def bidding_strategy_path(customer_id: str,bidding_strategy_id: str,) -> str:
        """Returns a fully-qualified bidding_strategy string."""
        return "customers/{customer_id}/biddingStrategies/{bidding_strategy_id}".format(customer_id=customer_id, bidding_strategy_id=bidding_strategy_id, )

    @staticmethod
    def parse_bidding_strategy_path(path: str) -> Dict[str,str]:
        """Parses a bidding_strategy path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/biddingStrategies/(?P<bidding_strategy_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_path(customer_id: str,campaign_id: str,) -> str:
        """Returns a fully-qualified campaign string."""
        return "customers/{customer_id}/campaigns/{campaign_id}".format(customer_id=customer_id, campaign_id=campaign_id, )

    @staticmethod
    def parse_campaign_path(path: str) -> Dict[str,str]:
        """Parses a campaign path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaigns/(?P<campaign_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_asset_path(customer_id: str,campaign_id: str,asset_id: str,field_type: str,) -> str:
        """Returns a fully-qualified campaign_asset string."""
        return "customers/{customer_id}/campaignAssets/{campaign_id}~{asset_id}~{field_type}".format(customer_id=customer_id, campaign_id=campaign_id, asset_id=asset_id, field_type=field_type, )

    @staticmethod
    def parse_campaign_asset_path(path: str) -> Dict[str,str]:
        """Parses a campaign_asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignAssets/(?P<campaign_id>.+?)~(?P<asset_id>.+?)~(?P<field_type>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_asset_set_path(customer_id: str,campaign_id: str,asset_set_id: str,) -> str:
        """Returns a fully-qualified campaign_asset_set string."""
        return "customers/{customer_id}/campaignAssetSets/{campaign_id}~{asset_set_id}".format(customer_id=customer_id, campaign_id=campaign_id, asset_set_id=asset_set_id, )

    @staticmethod
    def parse_campaign_asset_set_path(path: str) -> Dict[str,str]:
        """Parses a campaign_asset_set path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignAssetSets/(?P<campaign_id>.+?)~(?P<asset_set_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_audience_view_path(customer_id: str,campaign_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified campaign_audience_view string."""
        return "customers/{customer_id}/campaignAudienceViews/{campaign_id}~{criterion_id}".format(customer_id=customer_id, campaign_id=campaign_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_campaign_audience_view_path(path: str) -> Dict[str,str]:
        """Parses a campaign_audience_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignAudienceViews/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_budget_path(customer_id: str,budget_id: str,) -> str:
        """Returns a fully-qualified campaign_budget string."""
        return "customers/{customer_id}/campaignBudgets/{budget_id}".format(customer_id=customer_id, budget_id=budget_id, )

    @staticmethod
    def parse_campaign_budget_path(path: str) -> Dict[str,str]:
        """Parses a campaign_budget path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignBudgets/(?P<budget_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_criterion_path(customer_id: str,campaign_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified campaign_criterion string."""
        return "customers/{customer_id}/campaignCriteria/{campaign_id}~{criterion_id}".format(customer_id=customer_id, campaign_id=campaign_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_campaign_criterion_path(path: str) -> Dict[str,str]:
        """Parses a campaign_criterion path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignCriteria/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_label_path(customer_id: str,campaign_id: str,entity_id: str,) -> str:
        """Returns a fully-qualified campaign_label string."""
        return "customers/{customer_id}/campaignLabels/{campaign_id}~{entity_id}".format(customer_id=customer_id, campaign_id=campaign_id, entity_id=entity_id, )

    @staticmethod
    def parse_campaign_label_path(path: str) -> Dict[str,str]:
        """Parses a campaign_label path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/campaignLabels/(?P<campaign_id>.+?)~(?P<entity_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def cart_data_sales_view_path(customer_id: str,) -> str:
        """Returns a fully-qualified cart_data_sales_view string."""
        return "customers/{customer_id}/cartDataSalesView".format(customer_id=customer_id, )

    @staticmethod
    def parse_cart_data_sales_view_path(path: str) -> Dict[str,str]:
        """Parses a cart_data_sales_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/cartDataSalesView$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_path(customer_id: str,ad_group_id: str,criteria_id: str,ds_conversion_id: str,) -> str:
        """Returns a fully-qualified conversion string."""
        return "customers/{customer_id}/conversions/{ad_group_id}~{criteria_id}~{ds_conversion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criteria_id=criteria_id, ds_conversion_id=ds_conversion_id, )

    @staticmethod
    def parse_conversion_path(path: str) -> Dict[str,str]:
        """Parses a conversion path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/conversions/(?P<ad_group_id>.+?)~(?P<criteria_id>.+?)~(?P<ds_conversion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_action_path(customer_id: str,conversion_type_id: str,) -> str:
        """Returns a fully-qualified conversion_action string."""
        return "customers/{customer_id}/conversionActions/{conversion_type_id}".format(customer_id=customer_id, conversion_type_id=conversion_type_id, )

    @staticmethod
    def parse_conversion_action_path(path: str) -> Dict[str,str]:
        """Parses a conversion_action path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/conversionActions/(?P<conversion_type_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_custom_variable_path(customer_id: str,conversion_custom_variable_id: str,) -> str:
        """Returns a fully-qualified conversion_custom_variable string."""
        return "customers/{customer_id}/conversionCustomVariables/{conversion_custom_variable_id}".format(customer_id=customer_id, conversion_custom_variable_id=conversion_custom_variable_id, )

    @staticmethod
    def parse_conversion_custom_variable_path(path: str) -> Dict[str,str]:
        """Parses a conversion_custom_variable path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/conversionCustomVariables/(?P<conversion_custom_variable_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_path(customer_id: str,) -> str:
        """Returns a fully-qualified customer string."""
        return "customers/{customer_id}".format(customer_id=customer_id, )

    @staticmethod
    def parse_customer_path(path: str) -> Dict[str,str]:
        """Parses a customer path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_asset_path(customer_id: str,asset_id: str,field_type: str,) -> str:
        """Returns a fully-qualified customer_asset string."""
        return "customers/{customer_id}/customerAssets/{asset_id}~{field_type}".format(customer_id=customer_id, asset_id=asset_id, field_type=field_type, )

    @staticmethod
    def parse_customer_asset_path(path: str) -> Dict[str,str]:
        """Parses a customer_asset path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/customerAssets/(?P<asset_id>.+?)~(?P<field_type>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_asset_set_path(customer_id: str,asset_set_id: str,) -> str:
        """Returns a fully-qualified customer_asset_set string."""
        return "customers/{customer_id}/customerAssetSets/{asset_set_id}".format(customer_id=customer_id, asset_set_id=asset_set_id, )

    @staticmethod
    def parse_customer_asset_set_path(path: str) -> Dict[str,str]:
        """Parses a customer_asset_set path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/customerAssetSets/(?P<asset_set_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_client_path(customer_id: str,client_external_customer_id: str,) -> str:
        """Returns a fully-qualified customer_client string."""
        return "customers/{customer_id}/customerClients/{client_external_customer_id}".format(customer_id=customer_id, client_external_customer_id=client_external_customer_id, )

    @staticmethod
    def parse_customer_client_path(path: str) -> Dict[str,str]:
        """Parses a customer_client path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/customerClients/(?P<client_external_customer_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_manager_link_path(customer_id: str,manager_customer_id: str,manager_link_id: str,) -> str:
        """Returns a fully-qualified customer_manager_link string."""
        return "customers/{customer_id}/customerManagerLinks/{manager_customer_id}~{manager_link_id}".format(customer_id=customer_id, manager_customer_id=manager_customer_id, manager_link_id=manager_link_id, )

    @staticmethod
    def parse_customer_manager_link_path(path: str) -> Dict[str,str]:
        """Parses a customer_manager_link path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/customerManagerLinks/(?P<manager_customer_id>.+?)~(?P<manager_link_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def dynamic_search_ads_search_term_view_path(customer_id: str,ad_group_id: str,query_fp: str,line1_fp: str,url_fp: str,feed_item_lp_url_fp: str,) -> str:
        """Returns a fully-qualified dynamic_search_ads_search_term_view string."""
        return "customers/{customer_id}/dynamicSearchAdsSearchTermViews/{ad_group_id}~{query_fp}~{line1_fp}~{url_fp}~{feed_item_lp_url_fp}".format(customer_id=customer_id, ad_group_id=ad_group_id, query_fp=query_fp, line1_fp=line1_fp, url_fp=url_fp, feed_item_lp_url_fp=feed_item_lp_url_fp, )

    @staticmethod
    def parse_dynamic_search_ads_search_term_view_path(path: str) -> Dict[str,str]:
        """Parses a dynamic_search_ads_search_term_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/dynamicSearchAdsSearchTermViews/(?P<ad_group_id>.+?)~(?P<query_fp>.+?)~(?P<line1_fp>.+?)~(?P<url_fp>.+?)~(?P<feed_item_lp_url_fp>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def gender_view_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified gender_view string."""
        return "customers/{customer_id}/genderViews/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_gender_view_path(path: str) -> Dict[str,str]:
        """Parses a gender_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/genderViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def geo_target_constant_path(criterion_id: str,) -> str:
        """Returns a fully-qualified geo_target_constant string."""
        return "geoTargetConstants/{criterion_id}".format(criterion_id=criterion_id, )

    @staticmethod
    def parse_geo_target_constant_path(path: str) -> Dict[str,str]:
        """Parses a geo_target_constant path into its component segments."""
        m = re.match(r"^geoTargetConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_view_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified keyword_view string."""
        return "customers/{customer_id}/keywordViews/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_keyword_view_path(path: str) -> Dict[str,str]:
        """Parses a keyword_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/keywordViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def label_path(customer_id: str,label_id: str,) -> str:
        """Returns a fully-qualified label string."""
        return "customers/{customer_id}/labels/{label_id}".format(customer_id=customer_id, label_id=label_id, )

    @staticmethod
    def parse_label_path(path: str) -> Dict[str,str]:
        """Parses a label path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/labels/(?P<label_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def language_constant_path(criterion_id: str,) -> str:
        """Returns a fully-qualified language_constant string."""
        return "languageConstants/{criterion_id}".format(criterion_id=criterion_id, )

    @staticmethod
    def parse_language_constant_path(path: str) -> Dict[str,str]:
        """Parses a language_constant path into its component segments."""
        m = re.match(r"^languageConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def location_view_path(customer_id: str,campaign_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified location_view string."""
        return "customers/{customer_id}/locationViews/{campaign_id}~{criterion_id}".format(customer_id=customer_id, campaign_id=campaign_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_location_view_path(path: str) -> Dict[str,str]:
        """Parses a location_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/locationViews/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def product_bidding_category_constant_path(country_code: str,level: str,canonical_value: str,) -> str:
        """Returns a fully-qualified product_bidding_category_constant string."""
        return "productBiddingCategoryConstants/{country_code}~{level}~{canonical_value}".format(country_code=country_code, level=level, canonical_value=canonical_value, )

    @staticmethod
    def parse_product_bidding_category_constant_path(path: str) -> Dict[str,str]:
        """Parses a product_bidding_category_constant path into its component segments."""
        m = re.match(r"^productBiddingCategoryConstants/(?P<country_code>.+?)~(?P<level>.+?)~(?P<canonical_value>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def product_group_view_path(customer_id: str,adgroup_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified product_group_view string."""
        return "customers/{customer_id}/productGroupViews/{adgroup_id}~{criterion_id}".format(customer_id=customer_id, adgroup_id=adgroup_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_product_group_view_path(path: str) -> Dict[str,str]:
        """Parses a product_group_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/productGroupViews/(?P<adgroup_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def shopping_performance_view_path(customer_id: str,) -> str:
        """Returns a fully-qualified shopping_performance_view string."""
        return "customers/{customer_id}/shoppingPerformanceView".format(customer_id=customer_id, )

    @staticmethod
    def parse_shopping_performance_view_path(path: str) -> Dict[str,str]:
        """Parses a shopping_performance_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/shoppingPerformanceView$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def user_list_path(customer_id: str,user_list_id: str,) -> str:
        """Returns a fully-qualified user_list string."""
        return "customers/{customer_id}/userLists/{user_list_id}".format(customer_id=customer_id, user_list_id=user_list_id, )

    @staticmethod
    def parse_user_list_path(path: str) -> Dict[str,str]:
        """Parses a user_list path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/userLists/(?P<user_list_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def visit_path(customer_id: str,ad_group_id: str,criteria_id: str,ds_visit_id: str,) -> str:
        """Returns a fully-qualified visit string."""
        return "customers/{customer_id}/visits/{ad_group_id}~{criteria_id}~{ds_visit_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criteria_id=criteria_id, ds_visit_id=ds_visit_id, )

    @staticmethod
    def parse_visit_path(path: str) -> Dict[str,str]:
        """Parses a visit path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/visits/(?P<ad_group_id>.+?)~(?P<criteria_id>.+?)~(?P<ds_visit_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def webpage_view_path(customer_id: str,ad_group_id: str,criterion_id: str,) -> str:
        """Returns a fully-qualified webpage_view string."""
        return "customers/{customer_id}/webpageViews/{ad_group_id}~{criterion_id}".format(customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id, )

    @staticmethod
    def parse_webpage_view_path(path: str) -> Dict[str,str]:
        """Parses a webpage_view path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)/webpageViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str, ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(billing_account=billing_account, )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str,str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str, ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder, )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str,str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str, ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization, )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str,str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str, ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str,str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str, ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(project=project, location=location, )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str,str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Optional[Union[str, SearchAds360ServiceTransport]] = None,
            client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the search ads360 service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str, SearchAds360ServiceTransport]]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        # Create SSL credentials for mutual TLS if needed.
        if os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true"

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, SearchAds360ServiceTransport):
            # transport is a SearchAds360ServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError("When providing a transport instance, "
                                 "provide its credentials directly.")
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
              )

    def search(self,
            request: Optional[Union[search_ads360_service.SearchSearchAds360Request, dict]] = None,
            *,
            customer_id: Optional[str] = None,
            query: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.SearchPager:
        r"""Returns all rows that match the search query.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QueryError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Args:
            request (Union[google.ads.searchads360.v0.services.types.SearchSearchAds360Request, dict, None]):
                The request object. Request message for
                [SearchAds360Service.Search][google.ads.searchads360.v0.services.SearchAds360Service.Search].
            customer_id (str):
                Required. The ID of the customer
                being queried.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (str):
                Required. The query string.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.searchads360.v0.services.services.search_ads360_service.pagers.SearchPager:
                Response message for
                   [SearchAds360Service.Search][google.ads.searchads360.v0.services.SearchAds360Service.Search].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([customer_id, query])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a search_ads360_service.SearchSearchAds360Request.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, search_ads360_service.SearchSearchAds360Request):
            request = search_ads360_service.SearchSearchAds360Request(request)
             # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("customer_id", request.customer_id),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_stream(self,
            request: Optional[Union[search_ads360_service.SearchSearchAds360StreamRequest, dict]] = None,
            *,
            customer_id: Optional[str] = None,
            query: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> Iterable[search_ads360_service.SearchSearchAds360StreamResponse]:
        r"""Returns all rows that match the search stream query.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QueryError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Args:
            request (Union[google.ads.searchads360.v0.services.types.SearchSearchAds360StreamRequest, dict, None]):
                The request object. Request message for
                [SearchAds360Service.SearchStream][google.ads.searchads360.v0.services.SearchAds360Service.SearchStream].
            customer_id (str):
                Required. The ID of the customer
                being queried.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (str):
                Required. The query string.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.ads.searchads360.v0.services.types.SearchSearchAds360StreamResponse]:
                Response message for
                   [SearchAds360Service.SearchStream][google.ads.searchads360.v0.services.SearchAds360Service.SearchStream].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([customer_id, query])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a search_ads360_service.SearchSearchAds360StreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, search_ads360_service.SearchSearchAds360StreamRequest):
            request = search_ads360_service.SearchSearchAds360StreamRequest(request)
             # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("customer_id", request.customer_id),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response










DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "SearchAds360ServiceClient",
)
