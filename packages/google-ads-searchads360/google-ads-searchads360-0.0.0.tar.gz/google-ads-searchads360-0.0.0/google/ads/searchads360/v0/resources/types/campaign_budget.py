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

from google.ads.searchads360.v0.enums.types import budget_delivery_method
from google.ads.searchads360.v0.enums.types import budget_period


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'CampaignBudget',
    },
)


class CampaignBudget(proto.Message):
    r"""A campaign budget.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign budget.
            Campaign budget resource names have the form:

            ``customers/{customer_id}/campaignBudgets/{campaign_budget_id}``
        amount_micros (int):
            The amount of the budget, in the local
            currency for the account. Amount is specified in
            micros, where one million is equivalent to one
            currency unit. Monthly spend is capped at 30.4
            times this amount.

            This field is a member of `oneof`_ ``_amount_micros``.
        delivery_method (google.ads.searchads360.v0.enums.types.BudgetDeliveryMethodEnum.BudgetDeliveryMethod):
            The delivery method that determines the rate
            at which the campaign budget is spent.

            Defaults to STANDARD if unspecified in a create
            operation.
        period (google.ads.searchads360.v0.enums.types.BudgetPeriodEnum.BudgetPeriod):
            Immutable. Period over which to spend the
            budget. Defaults to DAILY if not specified.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    amount_micros: int = proto.Field(
        proto.INT64,
        number=21,
        optional=True,
    )
    delivery_method: budget_delivery_method.BudgetDeliveryMethodEnum.BudgetDeliveryMethod = proto.Field(
        proto.ENUM,
        number=7,
        enum=budget_delivery_method.BudgetDeliveryMethodEnum.BudgetDeliveryMethod,
    )
    period: budget_period.BudgetPeriodEnum.BudgetPeriod = proto.Field(
        proto.ENUM,
        number=13,
        enum=budget_period.BudgetPeriodEnum.BudgetPeriod,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
