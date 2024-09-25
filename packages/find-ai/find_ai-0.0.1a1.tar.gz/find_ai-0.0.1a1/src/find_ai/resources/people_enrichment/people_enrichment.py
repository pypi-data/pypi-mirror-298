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

__all__ = ["PeopleEnrichmentResource", "AsyncPeopleEnrichmentResource"]


class PeopleEnrichmentResource(SyncAPIResource):
    @cached_property
    def enrich(self) -> EnrichResource:
        return EnrichResource(self._client)

    @cached_property
    def with_raw_response(self) -> PeopleEnrichmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return PeopleEnrichmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PeopleEnrichmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return PeopleEnrichmentResourceWithStreamingResponse(self)


class AsyncPeopleEnrichmentResource(AsyncAPIResource):
    @cached_property
    def enrich(self) -> AsyncEnrichResource:
        return AsyncEnrichResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPeopleEnrichmentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Find-AI/find-ai-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPeopleEnrichmentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPeopleEnrichmentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Find-AI/find-ai-python#with_streaming_response
        """
        return AsyncPeopleEnrichmentResourceWithStreamingResponse(self)


class PeopleEnrichmentResourceWithRawResponse:
    def __init__(self, people_enrichment: PeopleEnrichmentResource) -> None:
        self._people_enrichment = people_enrichment

    @cached_property
    def enrich(self) -> EnrichResourceWithRawResponse:
        return EnrichResourceWithRawResponse(self._people_enrichment.enrich)


class AsyncPeopleEnrichmentResourceWithRawResponse:
    def __init__(self, people_enrichment: AsyncPeopleEnrichmentResource) -> None:
        self._people_enrichment = people_enrichment

    @cached_property
    def enrich(self) -> AsyncEnrichResourceWithRawResponse:
        return AsyncEnrichResourceWithRawResponse(self._people_enrichment.enrich)


class PeopleEnrichmentResourceWithStreamingResponse:
    def __init__(self, people_enrichment: PeopleEnrichmentResource) -> None:
        self._people_enrichment = people_enrichment

    @cached_property
    def enrich(self) -> EnrichResourceWithStreamingResponse:
        return EnrichResourceWithStreamingResponse(self._people_enrichment.enrich)


class AsyncPeopleEnrichmentResourceWithStreamingResponse:
    def __init__(self, people_enrichment: AsyncPeopleEnrichmentResource) -> None:
        self._people_enrichment = people_enrichment

    @cached_property
    def enrich(self) -> AsyncEnrichResourceWithStreamingResponse:
        return AsyncEnrichResourceWithStreamingResponse(self._people_enrichment.enrich)
