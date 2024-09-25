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

from google.ads.searchads360.v0.resources.types import search_ads360_field


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.services',
    marshal='google.ads.searchads360.v0',
    manifest={
        'GetSearchAds360FieldRequest',
        'SearchSearchAds360FieldsRequest',
        'SearchSearchAds360FieldsResponse',
    },
)


class GetSearchAds360FieldRequest(proto.Message):
    r"""Request message for
    [SearchAds360FieldService.GetSearchAds360Field][google.ads.searchads360.v0.services.SearchAds360FieldService.GetSearchAds360Field].

    Attributes:
        resource_name (str):
            Required. The resource name of the field to
            get.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SearchSearchAds360FieldsRequest(proto.Message):
    r"""Request message for
    [SearchAds360FieldService.SearchSearchAds360Fields][google.ads.searchads360.v0.services.SearchAds360FieldService.SearchSearchAds360Fields].

    Attributes:
        query (str):
            Required. The query string.
        page_token (str):
            Token of the page to retrieve. If not specified, the first
            page of results will be returned. Use the value obtained
            from ``next_page_token`` in the previous response in order
            to request the next page of results.
        page_size (int):
            Number of elements to retrieve in a single
            page. When too large a page is requested, the
            server may decide to further limit the number of
            returned resources.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class SearchSearchAds360FieldsResponse(proto.Message):
    r"""Response message for
    [SearchAds360FieldService.SearchSearchAds360Fields][google.ads.searchads360.v0.services.SearchAds360FieldService.SearchSearchAds360Fields].

    Attributes:
        results (MutableSequence[google.ads.searchads360.v0.resources.types.SearchAds360Field]):
            The list of fields that matched the query.
        next_page_token (str):
            Pagination token used to retrieve the next page of results.
            Pass the content of this string as the ``page_token``
            attribute of the next request. ``next_page_token`` is not
            returned for the last page.
        total_results_count (int):
            Total number of results that match the query
            ignoring the LIMIT clause.
    """

    @property
    def raw_page(self):
        return self

    results: MutableSequence[search_ads360_field.SearchAds360Field] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=search_ads360_field.SearchAds360Field,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_results_count: int = proto.Field(
        proto.INT64,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
