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
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Audience',
    },
)


class Audience(proto.Message):
    r"""Audience is an effective targeting option that lets you
    intersect different segment attributes, such as detailed
    demographics and affinities, to create audiences that represent
    sections of your target segments.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the audience. Audience names
            have the form:

            ``customers/{customer_id}/audiences/{audience_id}``
        id (int):
            Output only. ID of the audience.
        name (str):
            Required. Name of the audience. It should be
            unique across all audiences. It must have a
            minimum length of 1 and maximum length of 255.
        description (str):
            Description of this audience.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
