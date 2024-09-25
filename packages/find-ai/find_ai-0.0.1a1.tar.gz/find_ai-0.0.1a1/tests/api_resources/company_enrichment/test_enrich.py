# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from find_ai import FindAI, AsyncFindAI
from find_ai._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnrich:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = client.company_enrichment.enrich.create()
        assert enrich.is_closed
        assert enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = client.company_enrichment.enrich.create(
            domain="domain",
        )
        assert enrich.is_closed
        assert enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        enrich = client.company_enrichment.enrich.with_raw_response.create()

        assert enrich.is_closed is True
        assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"
        assert enrich.json() == {"foo": "bar"}
        assert isinstance(enrich, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.company_enrichment.enrich.with_streaming_response.create() as enrich:
            assert not enrich.is_closed
            assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"

            assert enrich.json() == {"foo": "bar"}
            assert cast(Any, enrich.is_closed) is True
            assert isinstance(enrich, StreamedBinaryAPIResponse)

        assert cast(Any, enrich.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = client.company_enrichment.enrich.retrieve(
            "token",
        )
        assert enrich.is_closed
        assert enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        enrich = client.company_enrichment.enrich.with_raw_response.retrieve(
            "token",
        )

        assert enrich.is_closed is True
        assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"
        assert enrich.json() == {"foo": "bar"}
        assert isinstance(enrich, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, client: FindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.company_enrichment.enrich.with_streaming_response.retrieve(
            "token",
        ) as enrich:
            assert not enrich.is_closed
            assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"

            assert enrich.json() == {"foo": "bar"}
            assert cast(Any, enrich.is_closed) is True
            assert isinstance(enrich, StreamedBinaryAPIResponse)

        assert cast(Any, enrich.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_retrieve(self, client: FindAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token` but received ''"):
            client.company_enrichment.enrich.with_raw_response.retrieve(
                "",
            )


class TestAsyncEnrich:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = await async_client.company_enrichment.enrich.create()
        assert enrich.is_closed
        assert await enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create_with_all_params(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = await async_client.company_enrichment.enrich.create(
            domain="domain",
        )
        assert enrich.is_closed
        assert await enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        enrich = await async_client.company_enrichment.enrich.with_raw_response.create()

        assert enrich.is_closed is True
        assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await enrich.json() == {"foo": "bar"}
        assert isinstance(enrich, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/companies/enrich").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.company_enrichment.enrich.with_streaming_response.create() as enrich:
            assert not enrich.is_closed
            assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await enrich.json() == {"foo": "bar"}
            assert cast(Any, enrich.is_closed) is True
            assert isinstance(enrich, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, enrich.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        enrich = await async_client.company_enrichment.enrich.retrieve(
            "token",
        )
        assert enrich.is_closed
        assert await enrich.json() == {"foo": "bar"}
        assert cast(Any, enrich.is_closed) is True
        assert isinstance(enrich, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        enrich = await async_client.company_enrichment.enrich.with_raw_response.retrieve(
            "token",
        )

        assert enrich.is_closed is True
        assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await enrich.json() == {"foo": "bar"}
        assert isinstance(enrich, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, async_client: AsyncFindAI, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/companies/enrich/token").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.company_enrichment.enrich.with_streaming_response.retrieve(
            "token",
        ) as enrich:
            assert not enrich.is_closed
            assert enrich.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await enrich.json() == {"foo": "bar"}
            assert cast(Any, enrich.is_closed) is True
            assert isinstance(enrich, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, enrich.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_retrieve(self, async_client: AsyncFindAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `token` but received ''"):
            await async_client.company_enrichment.enrich.with_raw_response.retrieve(
                "",
            )
