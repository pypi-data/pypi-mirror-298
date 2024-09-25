# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .enrich import (
    EnrichResource,
    AsyncEnrichResource,
    EnrichResourceWithRawResponse,
    AsyncEnrichResourceWithRawResponse,
    EnrichResourceWithStreamingResponse,
    AsyncEnrichResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CompanyEnrichmentResource", "AsyncCompanyEnrichmentResource"]


class CompanyEnrichmentResource(SyncAPIResource):
    @cached_property
    def enrich(self) -> EnrichResource:
        return EnrichResource(self._client)

    @cached_property
    def with_raw_response(self) -> CompanyEnrichmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return CompanyEnrichmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompanyEnrichmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return CompanyEnrichmentResourceWithStreamingResponse(self)


class AsyncCompanyEnrichmentResource(AsyncAPIResource):
    @cached_property
    def enrich(self) -> AsyncEnrichResource:
        return AsyncEnrichResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCompanyEnrichmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompanyEnrichmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompanyEnrichmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return AsyncCompanyEnrichmentResourceWithStreamingResponse(self)


class CompanyEnrichmentResourceWithRawResponse:
    def __init__(self, company_enrichment: CompanyEnrichmentResource) -> None:
        self._company_enrichment = company_enrichment

    @cached_property
    def enrich(self) -> EnrichResourceWithRawResponse:
        return EnrichResourceWithRawResponse(self._company_enrichment.enrich)


class AsyncCompanyEnrichmentResourceWithRawResponse:
    def __init__(self, company_enrichment: AsyncCompanyEnrichmentResource) -> None:
        self._company_enrichment = company_enrichment

    @cached_property
    def enrich(self) -> AsyncEnrichResourceWithRawResponse:
        return AsyncEnrichResourceWithRawResponse(self._company_enrichment.enrich)


class CompanyEnrichmentResourceWithStreamingResponse:
    def __init__(self, company_enrichment: CompanyEnrichmentResource) -> None:
        self._company_enrichment = company_enrichment

    @cached_property
    def enrich(self) -> EnrichResourceWithStreamingResponse:
        return EnrichResourceWithStreamingResponse(self._company_enrichment.enrich)


class AsyncCompanyEnrichmentResourceWithStreamingResponse:
    def __init__(self, company_enrichment: AsyncCompanyEnrichmentResource) -> None:
        self._company_enrichment = company_enrichment

    @cached_property
    def enrich(self) -> AsyncEnrichResourceWithStreamingResponse:
        return AsyncEnrichResourceWithStreamingResponse(self._company_enrichment.enrich)
