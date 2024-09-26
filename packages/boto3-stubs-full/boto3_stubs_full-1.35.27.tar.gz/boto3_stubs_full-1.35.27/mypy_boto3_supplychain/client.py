"""
Type annotations for supplychain service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_supplychain.client import SupplyChainClient

    session = Session()
    client: SupplyChainClient = session.client("supplychain")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateBillOfMaterialsImportJobRequestRequestTypeDef,
    CreateBillOfMaterialsImportJobResponseTypeDef,
    GetBillOfMaterialsImportJobRequestRequestTypeDef,
    GetBillOfMaterialsImportJobResponseTypeDef,
    SendDataIntegrationEventRequestRequestTypeDef,
    SendDataIntegrationEventResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SupplyChainClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SupplyChainClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupplyChainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#close)
        """

    def create_bill_of_materials_import_job(
        self, **kwargs: Unpack[CreateBillOfMaterialsImportJobRequestRequestTypeDef]
    ) -> CreateBillOfMaterialsImportJobResponseTypeDef:
        """
        CreateBillOfMaterialsImportJob creates an import job for the Product Bill Of
        Materials (BOM)
        entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.create_bill_of_materials_import_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#create_bill_of_materials_import_job)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#generate_presigned_url)
        """

    def get_bill_of_materials_import_job(
        self, **kwargs: Unpack[GetBillOfMaterialsImportJobRequestRequestTypeDef]
    ) -> GetBillOfMaterialsImportJobResponseTypeDef:
        """
        Get status and details of a BillOfMaterialsImportJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.get_bill_of_materials_import_job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#get_bill_of_materials_import_job)
        """

    def send_data_integration_event(
        self, **kwargs: Unpack[SendDataIntegrationEventRequestRequestTypeDef]
    ) -> SendDataIntegrationEventResponseTypeDef:
        """
        Send the transactional data payload for the event with real-time data for
        analysis or
        monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client.send_data_integration_event)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/client/#send_data_integration_event)
        """
