"""
Type annotations for resource-groups service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/type_defs/)

Usage::

    ```python
    from mypy_boto3_resource_groups.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    GroupConfigurationStatusType,
    GroupFilterNameType,
    GroupLifecycleEventsDesiredStatusType,
    GroupLifecycleEventsStatusType,
    QueryErrorCodeType,
    QueryTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountSettingsTypeDef",
    "ResourceQueryTypeDef",
    "GroupTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteGroupInputRequestTypeDef",
    "FailedResourceTypeDef",
    "GetGroupConfigurationInputRequestTypeDef",
    "GetGroupInputRequestTypeDef",
    "GetGroupQueryInputRequestTypeDef",
    "GetTagsInputRequestTypeDef",
    "GroupConfigurationParameterOutputTypeDef",
    "GroupConfigurationParameterTypeDef",
    "GroupFilterTypeDef",
    "GroupIdentifierTypeDef",
    "GroupResourcesInputRequestTypeDef",
    "PendingResourceTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceFilterTypeDef",
    "ResourceIdentifierTypeDef",
    "ResourceStatusTypeDef",
    "QueryErrorTypeDef",
    "TagInputRequestTypeDef",
    "UngroupResourcesInputRequestTypeDef",
    "UntagInputRequestTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateGroupInputRequestTypeDef",
    "GroupQueryTypeDef",
    "SearchResourcesInputRequestTypeDef",
    "UpdateGroupQueryInputRequestTypeDef",
    "DeleteGroupOutputTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "GetGroupOutputTypeDef",
    "GetTagsOutputTypeDef",
    "TagOutputTypeDef",
    "UntagOutputTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "UpdateGroupOutputTypeDef",
    "GroupConfigurationItemOutputTypeDef",
    "GroupConfigurationParameterUnionTypeDef",
    "ListGroupsInputRequestTypeDef",
    "ListGroupsOutputTypeDef",
    "GroupResourcesOutputTypeDef",
    "UngroupResourcesOutputTypeDef",
    "ListGroupsInputListGroupsPaginateTypeDef",
    "SearchResourcesInputSearchResourcesPaginateTypeDef",
    "ListGroupResourcesInputListGroupResourcesPaginateTypeDef",
    "ListGroupResourcesInputRequestTypeDef",
    "ListGroupResourcesItemTypeDef",
    "SearchResourcesOutputTypeDef",
    "GetGroupQueryOutputTypeDef",
    "UpdateGroupQueryOutputTypeDef",
    "GroupConfigurationTypeDef",
    "GroupConfigurationItemTypeDef",
    "ListGroupResourcesOutputTypeDef",
    "CreateGroupOutputTypeDef",
    "GetGroupConfigurationOutputTypeDef",
    "GroupConfigurationItemUnionTypeDef",
    "PutGroupConfigurationInputRequestTypeDef",
    "CreateGroupInputRequestTypeDef",
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "GroupLifecycleEventsDesiredStatus": NotRequired[GroupLifecycleEventsDesiredStatusType],
        "GroupLifecycleEventsStatus": NotRequired[GroupLifecycleEventsStatusType],
        "GroupLifecycleEventsStatusMessage": NotRequired[str],
    },
)
ResourceQueryTypeDef = TypedDict(
    "ResourceQueryTypeDef",
    {
        "Type": QueryTypeType,
        "Query": str,
    },
)
GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "GroupArn": str,
        "Name": str,
        "Description": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
DeleteGroupInputRequestTypeDef = TypedDict(
    "DeleteGroupInputRequestTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
    },
)
FailedResourceTypeDef = TypedDict(
    "FailedResourceTypeDef",
    {
        "ResourceArn": NotRequired[str],
        "ErrorMessage": NotRequired[str],
        "ErrorCode": NotRequired[str],
    },
)
GetGroupConfigurationInputRequestTypeDef = TypedDict(
    "GetGroupConfigurationInputRequestTypeDef",
    {
        "Group": NotRequired[str],
    },
)
GetGroupInputRequestTypeDef = TypedDict(
    "GetGroupInputRequestTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
    },
)
GetGroupQueryInputRequestTypeDef = TypedDict(
    "GetGroupQueryInputRequestTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
    },
)
GetTagsInputRequestTypeDef = TypedDict(
    "GetTagsInputRequestTypeDef",
    {
        "Arn": str,
    },
)
GroupConfigurationParameterOutputTypeDef = TypedDict(
    "GroupConfigurationParameterOutputTypeDef",
    {
        "Name": str,
        "Values": NotRequired[List[str]],
    },
)
GroupConfigurationParameterTypeDef = TypedDict(
    "GroupConfigurationParameterTypeDef",
    {
        "Name": str,
        "Values": NotRequired[Sequence[str]],
    },
)
GroupFilterTypeDef = TypedDict(
    "GroupFilterTypeDef",
    {
        "Name": GroupFilterNameType,
        "Values": Sequence[str],
    },
)
GroupIdentifierTypeDef = TypedDict(
    "GroupIdentifierTypeDef",
    {
        "GroupName": NotRequired[str],
        "GroupArn": NotRequired[str],
    },
)
GroupResourcesInputRequestTypeDef = TypedDict(
    "GroupResourcesInputRequestTypeDef",
    {
        "Group": str,
        "ResourceArns": Sequence[str],
    },
)
PendingResourceTypeDef = TypedDict(
    "PendingResourceTypeDef",
    {
        "ResourceArn": NotRequired[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ResourceFilterTypeDef = TypedDict(
    "ResourceFilterTypeDef",
    {
        "Name": Literal["resource-type"],
        "Values": Sequence[str],
    },
)
ResourceIdentifierTypeDef = TypedDict(
    "ResourceIdentifierTypeDef",
    {
        "ResourceArn": NotRequired[str],
        "ResourceType": NotRequired[str],
    },
)
ResourceStatusTypeDef = TypedDict(
    "ResourceStatusTypeDef",
    {
        "Name": NotRequired[Literal["PENDING"]],
    },
)
QueryErrorTypeDef = TypedDict(
    "QueryErrorTypeDef",
    {
        "ErrorCode": NotRequired[QueryErrorCodeType],
        "Message": NotRequired[str],
    },
)
TagInputRequestTypeDef = TypedDict(
    "TagInputRequestTypeDef",
    {
        "Arn": str,
        "Tags": Mapping[str, str],
    },
)
UngroupResourcesInputRequestTypeDef = TypedDict(
    "UngroupResourcesInputRequestTypeDef",
    {
        "Group": str,
        "ResourceArns": Sequence[str],
    },
)
UntagInputRequestTypeDef = TypedDict(
    "UntagInputRequestTypeDef",
    {
        "Arn": str,
        "Keys": Sequence[str],
    },
)
UpdateAccountSettingsInputRequestTypeDef = TypedDict(
    "UpdateAccountSettingsInputRequestTypeDef",
    {
        "GroupLifecycleEventsDesiredStatus": NotRequired[GroupLifecycleEventsDesiredStatusType],
    },
)
UpdateGroupInputRequestTypeDef = TypedDict(
    "UpdateGroupInputRequestTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
        "Description": NotRequired[str],
    },
)
GroupQueryTypeDef = TypedDict(
    "GroupQueryTypeDef",
    {
        "GroupName": str,
        "ResourceQuery": ResourceQueryTypeDef,
    },
)
SearchResourcesInputRequestTypeDef = TypedDict(
    "SearchResourcesInputRequestTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
UpdateGroupQueryInputRequestTypeDef = TypedDict(
    "UpdateGroupQueryInputRequestTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
    },
)
DeleteGroupOutputTypeDef = TypedDict(
    "DeleteGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAccountSettingsOutputTypeDef = TypedDict(
    "GetAccountSettingsOutputTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGroupOutputTypeDef = TypedDict(
    "GetGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTagsOutputTypeDef = TypedDict(
    "GetTagsOutputTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UntagOutputTypeDef = TypedDict(
    "UntagOutputTypeDef",
    {
        "Arn": str,
        "Keys": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAccountSettingsOutputTypeDef = TypedDict(
    "UpdateAccountSettingsOutputTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGroupOutputTypeDef = TypedDict(
    "UpdateGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GroupConfigurationItemOutputTypeDef = TypedDict(
    "GroupConfigurationItemOutputTypeDef",
    {
        "Type": str,
        "Parameters": NotRequired[List[GroupConfigurationParameterOutputTypeDef]],
    },
)
GroupConfigurationParameterUnionTypeDef = Union[
    GroupConfigurationParameterTypeDef, GroupConfigurationParameterOutputTypeDef
]
ListGroupsInputRequestTypeDef = TypedDict(
    "ListGroupsInputRequestTypeDef",
    {
        "Filters": NotRequired[Sequence[GroupFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListGroupsOutputTypeDef = TypedDict(
    "ListGroupsOutputTypeDef",
    {
        "GroupIdentifiers": List[GroupIdentifierTypeDef],
        "Groups": List[GroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GroupResourcesOutputTypeDef = TypedDict(
    "GroupResourcesOutputTypeDef",
    {
        "Succeeded": List[str],
        "Failed": List[FailedResourceTypeDef],
        "Pending": List[PendingResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UngroupResourcesOutputTypeDef = TypedDict(
    "UngroupResourcesOutputTypeDef",
    {
        "Succeeded": List[str],
        "Failed": List[FailedResourceTypeDef],
        "Pending": List[PendingResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListGroupsInputListGroupsPaginateTypeDef = TypedDict(
    "ListGroupsInputListGroupsPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[GroupFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchResourcesInputSearchResourcesPaginateTypeDef = TypedDict(
    "SearchResourcesInputSearchResourcesPaginateTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListGroupResourcesInputListGroupResourcesPaginateTypeDef = TypedDict(
    "ListGroupResourcesInputListGroupResourcesPaginateTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
        "Filters": NotRequired[Sequence[ResourceFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListGroupResourcesInputRequestTypeDef = TypedDict(
    "ListGroupResourcesInputRequestTypeDef",
    {
        "GroupName": NotRequired[str],
        "Group": NotRequired[str],
        "Filters": NotRequired[Sequence[ResourceFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListGroupResourcesItemTypeDef = TypedDict(
    "ListGroupResourcesItemTypeDef",
    {
        "Identifier": NotRequired[ResourceIdentifierTypeDef],
        "Status": NotRequired[ResourceStatusTypeDef],
    },
)
SearchResourcesOutputTypeDef = TypedDict(
    "SearchResourcesOutputTypeDef",
    {
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "QueryErrors": List[QueryErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetGroupQueryOutputTypeDef = TypedDict(
    "GetGroupQueryOutputTypeDef",
    {
        "GroupQuery": GroupQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGroupQueryOutputTypeDef = TypedDict(
    "UpdateGroupQueryOutputTypeDef",
    {
        "GroupQuery": GroupQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GroupConfigurationTypeDef = TypedDict(
    "GroupConfigurationTypeDef",
    {
        "Configuration": NotRequired[List[GroupConfigurationItemOutputTypeDef]],
        "ProposedConfiguration": NotRequired[List[GroupConfigurationItemOutputTypeDef]],
        "Status": NotRequired[GroupConfigurationStatusType],
        "FailureReason": NotRequired[str],
    },
)
GroupConfigurationItemTypeDef = TypedDict(
    "GroupConfigurationItemTypeDef",
    {
        "Type": str,
        "Parameters": NotRequired[Sequence[GroupConfigurationParameterUnionTypeDef]],
    },
)
ListGroupResourcesOutputTypeDef = TypedDict(
    "ListGroupResourcesOutputTypeDef",
    {
        "Resources": List[ListGroupResourcesItemTypeDef],
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "QueryErrors": List[QueryErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CreateGroupOutputTypeDef = TypedDict(
    "CreateGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResourceQuery": ResourceQueryTypeDef,
        "Tags": Dict[str, str],
        "GroupConfiguration": GroupConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGroupConfigurationOutputTypeDef = TypedDict(
    "GetGroupConfigurationOutputTypeDef",
    {
        "GroupConfiguration": GroupConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GroupConfigurationItemUnionTypeDef = Union[
    GroupConfigurationItemTypeDef, GroupConfigurationItemOutputTypeDef
]
PutGroupConfigurationInputRequestTypeDef = TypedDict(
    "PutGroupConfigurationInputRequestTypeDef",
    {
        "Group": NotRequired[str],
        "Configuration": NotRequired[Sequence[GroupConfigurationItemTypeDef]],
    },
)
CreateGroupInputRequestTypeDef = TypedDict(
    "CreateGroupInputRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "ResourceQuery": NotRequired[ResourceQueryTypeDef],
        "Tags": NotRequired[Mapping[str, str]],
        "Configuration": NotRequired[Sequence[GroupConfigurationItemUnionTypeDef]],
    },
)
