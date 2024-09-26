# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from find_ai import FindAI, AsyncFindAI
from tests.utils import assert_matches_type
from find_ai.types.people_enrichment import EnrichCreateResponse, EnrichRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnrich:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: FindAI) -> None:
        enrich = client.people_enrichment.enrich.create()
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: FindAI) -> None:
        enrich = client.people_enrichment.enrich.create(
            email="email",
        )
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: FindAI) -> None:
        response = client.people_enrichment.enrich.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrich = response.parse()
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: FindAI) -> None:
        with client.people_enrichment.enrich.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrich = response.parse()
            assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: FindAI) -> None:
        enrich = client.people_enrichment.enrich.retrieve(
            "token",
        )
        assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: FindAI) -> None:
        response = client.people_enrichment.enrich.with_raw_response.retrieve(
            "token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrich = response.parse()
        assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: FindAI) -> None:
        with client.people_enrichment.enrich.with_streaming_response.retrieve(
            "token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrich = response.parse()
            assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: FindAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token` but received ''"):
            client.people_enrichment.enrich.with_raw_response.retrieve(
                "",
            )


class TestAsyncEnrich:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncFindAI) -> None:
        enrich = await async_client.people_enrichment.enrich.create()
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncFindAI) -> None:
        enrich = await async_client.people_enrichment.enrich.create(
            email="email",
        )
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncFindAI) -> None:
        response = await async_client.people_enrichment.enrich.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrich = await response.parse()
        assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncFindAI) -> None:
        async with async_client.people_enrichment.enrich.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrich = await response.parse()
            assert_matches_type(EnrichCreateResponse, enrich, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFindAI) -> None:
        enrich = await async_client.people_enrichment.enrich.retrieve(
            "token",
        )
        assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFindAI) -> None:
        response = await async_client.people_enrichment.enrich.with_raw_response.retrieve(
            "token",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrich = await response.parse()
        assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFindAI) -> None:
        async with async_client.people_enrichment.enrich.with_streaming_response.retrieve(
            "token",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrich = await response.parse()
            assert_matches_type(EnrichRetrieveResponse, enrich, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncFindAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token` but received ''"):
            await async_client.people_enrichment.enrich.with_raw_response.retrieve(
                "",
            )
