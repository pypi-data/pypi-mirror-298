"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from ascend_sdk import utils
from ascend_sdk._hooks import HookContext
from ascend_sdk.models import components, errors, operations
from ascend_sdk.types import OptionalNullable, UNSET
from typing import Any, Optional


class CashBalances(BaseSDK):
    def calculate_cash_balance(
        self,
        *,
        account_id: str,
        mechanism: Optional[operations.Mechanism] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.CashBalancesCalculateCashBalanceResponse:
        r"""Get Cash Balance

        Calculates the cash balance for an account.

        :param account_id: The account id.
        :param mechanism: The withdraw mechanism to calculate the balance for. The mechanism determines what account activity will affect the balance.
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

        request = operations.CashBalancesCalculateCashBalanceRequest(
            account_id=account_id,
            mechanism=mechanism,
        )

        req = self.build_request(
            method="GET",
            path="/transfers/v1/accounts/{account_id}:calculateCashBalance",
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
                operation_id="CashBalances_CalculateCashBalance",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "4XX", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.CashBalancesCalculateCashBalanceResponse(
                calculate_cash_balance_response=utils.unmarshal_json(
                    http_res.text, Optional[components.CalculateCashBalanceResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(http_res, ["400", "403"], "application/json"):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.CashBalancesCalculateCashBalanceResponse(
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

    async def calculate_cash_balance_async(
        self,
        *,
        account_id: str,
        mechanism: Optional[operations.Mechanism] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> operations.CashBalancesCalculateCashBalanceResponse:
        r"""Get Cash Balance

        Calculates the cash balance for an account.

        :param account_id: The account id.
        :param mechanism: The withdraw mechanism to calculate the balance for. The mechanism determines what account activity will affect the balance.
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

        request = operations.CashBalancesCalculateCashBalanceRequest(
            account_id=account_id,
            mechanism=mechanism,
        )

        req = self.build_request(
            method="GET",
            path="/transfers/v1/accounts/{account_id}:calculateCashBalance",
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
                operation_id="CashBalances_CalculateCashBalance",
                oauth2_scopes=[],
                security_source=self.sdk_configuration.security,
            ),
            request=req,
            error_status_codes=["400", "403", "4XX", "5XX"],
            retry_config=retry_config,
        )

        data: Any = None
        if utils.match_response(http_res, "200", "application/json"):
            return operations.CashBalancesCalculateCashBalanceResponse(
                calculate_cash_balance_response=utils.unmarshal_json(
                    http_res.text, Optional[components.CalculateCashBalanceResponse]
                ),
                http_meta=components.HTTPMetadata(request=req, response=http_res),
            )
        if utils.match_response(http_res, ["400", "403"], "application/json"):
            data = utils.unmarshal_json(http_res.text, errors.StatusData)
            raise errors.Status(data=data)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            raise errors.SDKError(
                "API error occurred", http_res.status_code, http_res.text, http_res
            )
        if utils.match_response(http_res, "default", "application/json"):
            return operations.CashBalancesCalculateCashBalanceResponse(
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
