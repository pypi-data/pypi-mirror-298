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
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'AdTextAsset',
    },
)


class AdTextAsset(proto.Message):
    r"""A text asset used inside an ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            Asset text.

            This field is a member of `oneof`_ ``_text``.
    """

    text: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
