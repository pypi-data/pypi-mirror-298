# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.company_enrichment import enrich_create_params
from ...types.company_enrichment.enrich_create_response import EnrichCreateResponse
from ...types.company_enrichment.enrich_retrieve_response import EnrichRetrieveResponse

__all__ = ["EnrichResource", "AsyncEnrichResource"]


class EnrichResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnrichResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return EnrichResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnrichResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return EnrichResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        domain: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnrichCreateResponse:
        """
        Returns structured data about a company based on a domain input.

        Args:
          domain: The domain of the company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/companies/enrich",
            body=maybe_transform({"domain": domain}, enrich_create_params.EnrichCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnrichCreateResponse,
        )

    def retrieve(
        self,
        token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnrichRetrieveResponse:
        """
        The endpoint to poll to check the latest results when data about a company isn't
        immediately available.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not token:
            raise ValueError(f"Expected a non-empty value for `token` but received {token!r}")
        return self._get(
            f"/v1/companies/enrich/{token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnrichRetrieveResponse,
        )


class AsyncEnrichResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnrichResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEnrichResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnrichResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return AsyncEnrichResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        domain: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnrichCreateResponse:
        """
        Returns structured data about a company based on a domain input.

        Args:
          domain: The domain of the company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/companies/enrich",
            body=await async_maybe_transform({"domain": domain}, enrich_create_params.EnrichCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnrichCreateResponse,
        )

    async def retrieve(
        self,
        token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnrichRetrieveResponse:
        """
        The endpoint to poll to check the latest results when data about a company isn't
        immediately available.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not token:
            raise ValueError(f"Expected a non-empty value for `token` but received {token!r}")
        return await self._get(
            f"/v1/companies/enrich/{token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EnrichRetrieveResponse,
        )


class EnrichResourceWithRawResponse:
    def __init__(self, enrich: EnrichResource) -> None:
        self._enrich = enrich

        self.create = to_raw_response_wrapper(
            enrich.create,
        )
        self.retrieve = to_raw_response_wrapper(
            enrich.retrieve,
        )


class AsyncEnrichResourceWithRawResponse:
    def __init__(self, enrich: AsyncEnrichResource) -> None:
        self._enrich = enrich

        self.create = async_to_raw_response_wrapper(
            enrich.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            enrich.retrieve,
        )


class EnrichResourceWithStreamingResponse:
    def __init__(self, enrich: EnrichResource) -> None:
        self._enrich = enrich

        self.create = to_streamed_response_wrapper(
            enrich.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            enrich.retrieve,
        )


class AsyncEnrichResourceWithStreamingResponse:
    def __init__(self, enrich: AsyncEnrichResource) -> None:
        self._enrich = enrich

        self.create = async_to_streamed_response_wrapper(
            enrich.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            enrich.retrieve,
        )
