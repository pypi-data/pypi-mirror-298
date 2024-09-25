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


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.services',
    marshal='google.ads.searchads360.v0',
    manifest={
        'ListAccessibleCustomersRequest',
        'ListAccessibleCustomersResponse',
    },
)


class ListAccessibleCustomersRequest(proto.Message):
    r"""Request message for
    [CustomerService.ListAccessibleCustomers][google.ads.searchads360.v0.services.CustomerService.ListAccessibleCustomers].

    """


class ListAccessibleCustomersResponse(proto.Message):
    r"""Response message for
    [CustomerService.ListAccessibleCustomers][google.ads.searchads360.v0.services.CustomerService.ListAccessibleCustomers].

    Attributes:
        resource_names (MutableSequence[str]):
            Resource name of customers directly
            accessible by the user authenticating the call.
    """

    resource_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
