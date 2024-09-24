# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from copy import deepcopy
from typing import Any, Awaitable, TYPE_CHECKING
from typing_extensions import Self

from azure.core.pipeline import policies
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.mgmt.core import AsyncARMPipelineClient
from azure.mgmt.core.policies import AsyncARMAutoResourceProviderRegistrationPolicy

from .. import models as _models
from .._serialization import Deserializer, Serializer
from ._configuration import AVSClientConfiguration
from .operations import (
    AddonsOperations,
    AuthorizationsOperations,
    CloudLinksOperations,
    ClustersOperations,
    DatastoresOperations,
    GlobalReachConnectionsOperations,
    HcxEnterpriseSitesOperations,
    IscsiPathsOperations,
    LocationsOperations,
    Operations,
    PlacementPoliciesOperations,
    PrivateCloudsOperations,
    ScriptCmdletsOperations,
    ScriptExecutionsOperations,
    ScriptPackagesOperations,
    VirtualMachinesOperations,
    WorkloadNetworksOperations,
)

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials_async import AsyncTokenCredential


class AVSClient:  # pylint: disable=client-accepts-api-version-keyword,too-many-instance-attributes
    """Azure VMware Solution API.

    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.avs.aio.operations.Operations
    :ivar locations: LocationsOperations operations
    :vartype locations: azure.mgmt.avs.aio.operations.LocationsOperations
    :ivar private_clouds: PrivateCloudsOperations operations
    :vartype private_clouds: azure.mgmt.avs.aio.operations.PrivateCloudsOperations
    :ivar addons: AddonsOperations operations
    :vartype addons: azure.mgmt.avs.aio.operations.AddonsOperations
    :ivar authorizations: AuthorizationsOperations operations
    :vartype authorizations: azure.mgmt.avs.aio.operations.AuthorizationsOperations
    :ivar cloud_links: CloudLinksOperations operations
    :vartype cloud_links: azure.mgmt.avs.aio.operations.CloudLinksOperations
    :ivar clusters: ClustersOperations operations
    :vartype clusters: azure.mgmt.avs.aio.operations.ClustersOperations
    :ivar datastores: DatastoresOperations operations
    :vartype datastores: azure.mgmt.avs.aio.operations.DatastoresOperations
    :ivar placement_policies: PlacementPoliciesOperations operations
    :vartype placement_policies: azure.mgmt.avs.aio.operations.PlacementPoliciesOperations
    :ivar virtual_machines: VirtualMachinesOperations operations
    :vartype virtual_machines: azure.mgmt.avs.aio.operations.VirtualMachinesOperations
    :ivar global_reach_connections: GlobalReachConnectionsOperations operations
    :vartype global_reach_connections:
     azure.mgmt.avs.aio.operations.GlobalReachConnectionsOperations
    :ivar hcx_enterprise_sites: HcxEnterpriseSitesOperations operations
    :vartype hcx_enterprise_sites: azure.mgmt.avs.aio.operations.HcxEnterpriseSitesOperations
    :ivar iscsi_paths: IscsiPathsOperations operations
    :vartype iscsi_paths: azure.mgmt.avs.aio.operations.IscsiPathsOperations
    :ivar script_executions: ScriptExecutionsOperations operations
    :vartype script_executions: azure.mgmt.avs.aio.operations.ScriptExecutionsOperations
    :ivar script_packages: ScriptPackagesOperations operations
    :vartype script_packages: azure.mgmt.avs.aio.operations.ScriptPackagesOperations
    :ivar script_cmdlets: ScriptCmdletsOperations operations
    :vartype script_cmdlets: azure.mgmt.avs.aio.operations.ScriptCmdletsOperations
    :ivar workload_networks: WorkloadNetworksOperations operations
    :vartype workload_networks: azure.mgmt.avs.aio.operations.WorkloadNetworksOperations
    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials_async.AsyncTokenCredential
    :param subscription_id: The ID of the target subscription. The value must be an UUID. Required.
    :type subscription_id: str
    :param base_url: Service URL. Default value is "https://management.azure.com".
    :type base_url: str
    :keyword api_version: Api Version. Default value is "2023-09-01". Note that overriding this
     default value may result in unsupported behavior.
    :paramtype api_version: str
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
     Retry-After header is present.
    """

    def __init__(
        self,
        credential: "AsyncTokenCredential",
        subscription_id: str,
        base_url: str = "https://management.azure.com",
        **kwargs: Any
    ) -> None:
        self._config = AVSClientConfiguration(credential=credential, subscription_id=subscription_id, **kwargs)
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                policies.RequestIdPolicy(**kwargs),
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                AsyncARMAutoResourceProviderRegistrationPolicy(),
                self._config.redirect_policy,
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.custom_hook_policy,
                self._config.logging_policy,
                policies.DistributedTracingPolicy(**kwargs),
                policies.SensitiveHeaderCleanupPolicy(**kwargs) if self._config.redirect_policy else None,
                self._config.http_logging_policy,
            ]
        self._client: AsyncARMPipelineClient = AsyncARMPipelineClient(base_url=base_url, policies=_policies, **kwargs)

        client_models = {k: v for k, v in _models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._serialize.client_side_validation = False
        self.operations = Operations(self._client, self._config, self._serialize, self._deserialize)
        self.locations = LocationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.private_clouds = PrivateCloudsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.addons = AddonsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.authorizations = AuthorizationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.cloud_links = CloudLinksOperations(self._client, self._config, self._serialize, self._deserialize)
        self.clusters = ClustersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.datastores = DatastoresOperations(self._client, self._config, self._serialize, self._deserialize)
        self.placement_policies = PlacementPoliciesOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.virtual_machines = VirtualMachinesOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.global_reach_connections = GlobalReachConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.hcx_enterprise_sites = HcxEnterpriseSitesOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.iscsi_paths = IscsiPathsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.script_executions = ScriptExecutionsOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.script_packages = ScriptPackagesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.script_cmdlets = ScriptCmdletsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.workload_networks = WorkloadNetworksOperations(
            self._client, self._config, self._serialize, self._deserialize
        )

    def _send_request(
        self, request: HttpRequest, *, stream: bool = False, **kwargs: Any
    ) -> Awaitable[AsyncHttpResponse]:
        """Runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = await client._send_request(request)
        <AsyncHttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/dpcodegen/python/send_request

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """

        request_copy = deepcopy(request)
        request_copy.url = self._client.format_url(request_copy.url)
        return self._client.send_request(request_copy, stream=stream, **kwargs)  # type: ignore

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_details: Any) -> None:
        await self._client.__aexit__(*exc_details)
