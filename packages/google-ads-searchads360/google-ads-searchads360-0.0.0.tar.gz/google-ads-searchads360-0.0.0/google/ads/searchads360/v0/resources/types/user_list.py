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

from google.ads.searchads360.v0.enums.types import user_list_type


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.resources',
    marshal='google.ads.searchads360.v0',
    manifest={
        'UserList',
    },
)


class UserList(proto.Message):
    r"""A user list. This is a list of users a customer may target.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the user list. User list
            resource names have the form:

            ``customers/{customer_id}/userLists/{user_list_id}``
        id (int):
            Output only. Id of the user list.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            Name of this user list. Depending on its access_reason, the
            user list name may not be unique (for example, if
            access_reason=SHARED)

            This field is a member of `oneof`_ ``_name``.
        type_ (google.ads.searchads360.v0.enums.types.UserListTypeEnum.UserListType):
            Output only. Type of this list.

            This field is read-only.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=25,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=27,
        optional=True,
    )
    type_: user_list_type.UserListTypeEnum.UserListType = proto.Field(
        proto.ENUM,
        number=13,
        enum=user_list_type.UserListTypeEnum.UserListType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
