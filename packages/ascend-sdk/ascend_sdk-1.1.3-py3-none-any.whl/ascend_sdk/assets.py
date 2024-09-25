"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from ascend_sdk import utils
from ascend_sdk._hooks import HookContext
from ascend_sdk.models import components, errors, operations
from ascend_sdk.types import OptionalNullable, UNSET
from typing import Any, Optional


class Assets(BaseSDK):
    def list_assets(
        self,
        *,
        parent: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsListAssets1Response:
        r"""List Assets

        Lists assets

        :param parent: The parent resource name, which is the correspondent ID.
        :param page_size: The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)
        :param page_token: A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set.
        :param filter_: A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsListAssets1Request(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
            filter_=filter_,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/assets",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="Assets_ListAssets_1",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "504", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsListAssets1Response(
                list_assets_response=utils.unmarshal_json(
                    http_res.text, Optional[components.ListAssetsResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503", "504"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsListAssets1Response(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    async def list_assets_async(
        self,
        *,
        parent: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsListAssets1Response:
        r"""List Assets

        Lists assets

        :param parent: The parent resource name, which is the correspondent ID.
        :param page_size: The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)
        :param page_token: A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set.
        :param filter_: A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsListAssets1Request(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
            filter_=filter_,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/assets",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="Assets_ListAssets_1",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "504", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsListAssets1Response(
                list_assets_response=utils.unmarshal_json(
                    http_res.text, Optional[components.ListAssetsResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503", "504"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsListAssets1Response(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    def get_asset(
        self,
        *,
        asset_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsGetAssetResponse:
        r"""Get Asset

        Gets assets

        :param asset_id: The asset id.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsGetAssetRequest(
            asset_id=asset_id,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/assets/{asset_id}",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="Assets_GetAsset",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsGetAssetResponse(
                asset=utils.unmarshal_json(http_res.text, Optional[components.Asset]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsGetAssetResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    async def get_asset_async(
        self,
        *,
        asset_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsGetAssetResponse:
        r"""Get Asset

        Gets assets

        :param asset_id: The asset id.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsGetAssetRequest(
            asset_id=asset_id,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/assets/{asset_id}",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="Assets_GetAsset",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsGetAssetResponse(
                asset=utils.unmarshal_json(http_res.text, Optional[components.Asset]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsGetAssetResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    def list_assets_correspondent(
        self,
        *,
        correspondent_id: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsListAssetsCorrespondentResponse:
        r"""List Assets (By Correspondent)

        Lists assets

        :param correspondent_id: The correspondent id.
        :param page_size: The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)
        :param page_token: A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set.
        :param filter_: A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsListAssetsCorrespondentRequest(
            correspondent_id=correspondent_id,
            page_size=page_size,
            page_token=page_token,
            filter_=filter_,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/correspondents/{correspondent_id}/assets",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="Assets_ListAssets_Correspondent",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "504", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsListAssetsCorrespondentResponse(
                list_assets_response=utils.unmarshal_json(
                    http_res.text, Optional[components.ListAssetsResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503", "504"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsListAssetsCorrespondentResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    async def list_assets_correspondent_async(
        self,
        *,
        correspondent_id: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsListAssetsCorrespondentResponse:
        r"""List Assets (By Correspondent)

        Lists assets

        :param correspondent_id: The correspondent id.
        :param page_size: The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)
        :param page_token: A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set.
        :param filter_: A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsListAssetsCorrespondentRequest(
            correspondent_id=correspondent_id,
            page_size=page_size,
            page_token=page_token,
            filter_=filter_,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/correspondents/{correspondent_id}/assets",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="Assets_ListAssets_Correspondent",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "504", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsListAssetsCorrespondentResponse(
                list_assets_response=utils.unmarshal_json(
                    http_res.text, Optional[components.ListAssetsResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503", "504"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsListAssetsCorrespondentResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    def get_asset_correspondent(
        self,
        *,
        correspondent_id: str,
        asset_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsGetAssetCorrespondentResponse:
        r"""Get Asset (By Correspondent)

        Gets assets

        :param correspondent_id: The correspondent id.
        :param asset_id: The asset id.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsGetAssetCorrespondentRequest(
            correspondent_id=correspondent_id,
            asset_id=asset_id,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/correspondents/{correspondent_id}/assets/{asset_id}",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="Assets_GetAsset_Correspondent",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsGetAssetCorrespondentResponse(
                asset=utils.unmarshal_json(http_res.text, Optional[components.Asset]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsGetAssetCorrespondentResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )

    async def get_asset_correspondent_async(
        self,
        *,
        correspondent_id: str,
        asset_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.AssetsGetAssetCorrespondentResponse:
        r"""Get Asset (By Correspondent)

        Gets assets

        :param correspondent_id: The correspondent id.
        :param asset_id: The asset id.
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = operations.AssetsGetAssetCorrespondentRequest(
            correspondent_id=correspondent_id,
            asset_id=asset_id,
        )

        req = self.build_request(
            method="GET",
            path="/assets/v1/correspondents/{correspondent_id}/assets/{asset_id}",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="Assets_GetAsset_Correspondent",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "404", "4XX", "500", "503", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.AssetsGetAssetCorrespondentResponse(
                asset=utils.unmarshal_json(http_res.text, Optional[components.Asset]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(
            http_res, ["400", "403", "404", "500", "503"], "application/json"
        ):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.AssetsGetAssetCorrespondentResponse(
                status=utils.unmarshal_json(http_res.text, Optional[errors.Status]),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )

        content_type = http_res.headers.get("Content-Type")
        raise errors.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res.text,
            http_res,
        )
