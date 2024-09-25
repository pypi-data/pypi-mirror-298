"""Tests for the request client library."""

import aiohttp
import re
import pytest
from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro import field_options

from google_photos_library_api.auth import AbstractAuth
from google_photos_library_api.exceptions import (
    ApiException,
    ApiForbiddenException,
)

from .conftest import AuthCallback


@dataclass
class Response(DataClassJSONMixin):
    """Response from listing media items."""

    some_key: str = field(metadata=field_options(alias="some-key"))


class FakeAuth(AbstractAuth):
    """Implementation of AbstractAuth for use in tests."""

    async def async_get_access_token(self) -> str:
        """Return an OAuth credential for the calendar API."""
        return "some-token"


async def test_get_response(auth_cb: AuthCallback) -> None:
    """Test post that returns json."""

    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        body = await request.json()
        assert body == {"client_id": "some-client-id"}
        return aiohttp.web.json_response(
            {
                "some-key": "some-value",
            }
        )

    auth = await auth_cb([("/some-path", handler)])
    data = await auth.get("some-path", json={"client_id": "some-client-id"})
    assert await data.json() == {"some-key": "some-value"}


async def test_get_json_response_unexpected(auth_cb: AuthCallback) -> None:
    """Test json response with wrong response type."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.json_response(["value1", "value2"])

    @dataclass
    class Response(DataClassJSONMixin):
        """Response from listing media items."""

        items: list[str]

    auth = await auth_cb([("/some-path", handler)])
    with pytest.raises(ApiException):
        await auth.get_json("some-path", data_cls=Response)


async def test_get_json_response(auth_cb: AuthCallback) -> None:
    """Test post that returns json."""

    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        body = await request.json()
        assert body == {"client_id": "some-client-id"}
        return aiohttp.web.json_response(
            {
                "some-key": "some-value",
            }
        )

    auth = await auth_cb([("/some-path", handler)])
    data = await auth.get_json(
        "some-path", json={"client_id": "some-client-id"}, data_cls=Response
    )
    assert data == Response(some_key="some-value")


async def test_post_json_response(auth_cb: AuthCallback) -> None:
    """Test post that returns json."""

    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        body = await request.json()
        assert body == {"client_id": "some-client-id"}
        return aiohttp.web.json_response(
            {
                "some-key": "some-value",
            }
        )

    auth = await auth_cb([("/some-path", handler)])
    data = await auth.post_json(
        "some-path", json={"client_id": "some-client-id"}, data_cls=Response
    )
    assert data == Response(some_key="some-value")


async def test_post_json_response_unexpected(auth_cb: AuthCallback) -> None:
    """Test post that returns wrong json type."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.json_response(["value1", "value2"])

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(ApiException):
        await auth.post_json("some-path", data_cls=Response)


async def test_post_json_response_unexpected_text(auth_cb: AuthCallback) -> None:
    """Test post that returns unexpected format."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.Response(text="body")

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(ApiException):
        await auth.post_json("some-path", data_cls=Response)


async def test_get_json_response_bad_request(auth_cb: AuthCallback) -> None:
    """Test error handling with detailed json response."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.json_response(
            {
                "error": {
                    "errors": [
                        {
                            "domain": "calendar",
                            "reason": "timeRangeEmpty",
                            "message": "The specified time range is empty.",
                            "locationType": "parameter",
                            "location": "timeMax",
                        }
                    ],
                    "code": 400,
                    "message": "The specified time range is empty.",
                }
            },
            status=400,
        )

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(
        ApiException,
        match=re.escape(
            "Bad Request response from API (400): 400: The specified time range is empty."
        ),
    ):
        await auth.get("some-path")

    with pytest.raises(
        ApiException,
        match=re.escape(
            "Bad Request response from API (400): 400: The specified time range is empty."
        ),
    ):
        await auth.get_json("some-path", data_cls=Response)

    with pytest.raises(
        ApiException,
        match=re.escape(
            "Bad Request response from API (400): 400: The specified time range is empty."
        ),
    ):
        await auth.post("some-path")

    with pytest.raises(
        ApiException,
        match=re.escape(
            "Bad Request response from API (400): 400: The specified time range is empty."
        ),
    ):
        await auth.post_json("some-path", data_cls=Response)


async def test_unavailable_error(auth_cb: AuthCallback) -> None:
    """Test of basic request/response handling."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.Response(status=500)

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(ApiException):
        await auth.get_json("some-path", data_cls=Response)


async def test_forbidden_error(auth_cb: AuthCallback) -> None:
    """Test request/response handling for 403 status."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.json_response(
            {
                "error": {
                    "code": 403,
                    "message": "Google Photos API has not been used in project 0 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/library/photoslibrary.googleapis.com/overview?project=0 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.",
                    "status": "PERMISSION_DENIED",
                }
            },
            status=403,
        )

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(
        ApiForbiddenException,
        match=re.escape(
            "Forbidden response from API (403): PERMISSION_DENIED (403): Google Photos API has not been used in project 0 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/library/photoslibrary.googleapis.com/overview?project=0 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry."
        ),
    ):
        await auth.get_json("some-path", data_cls=Response)


async def test_error_detail_parse_error(auth_cb: AuthCallback) -> None:
    """Test request/response handling for 403 status."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.Response(status=403, text="Plain text error message")

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(
        ApiForbiddenException, match=re.escape("Forbidden response from API (403)")
    ):
        await auth.get_json("some-path", data_cls=Response)


async def test_invalid_argument(auth_cb: AuthCallback) -> None:
    """Test request/response handling for 403 status."""

    async def handler(_: aiohttp.web.Request) -> aiohttp.web.Response:
        return aiohttp.web.json_response(
            {
                "error": {
                    "code": 400,
                    "message": "Request contains an invalid argument.",
                    "status": "INVALID_ARGUMENT",
                    "details": [
                        {
                            "@type": "type.googleapis.com/google.rpc.BadRequest",
                            "fieldViolations": [
                                {
                                    "field": "id,baseUrl,mimeType,filename,mediaMetadata(width,height,photo,video)",
                                    "description": "Error expanding 'fields' parameter. Cannot find matching fields for path 'id'."
                                }
                            ]
                        }
                    ]
                }
            },
            status=400,
        )

    auth = await auth_cb([("/some-path", handler)])

    with pytest.raises(
        ApiException,
        match=re.escape(
            "Bad Request response from API (400): INVALID_ARGUMENT (400): Request contains an invalid argument."
        ) + "\nError details: .*",
    ):
        await auth.get_json("some-path", data_cls=Response)
