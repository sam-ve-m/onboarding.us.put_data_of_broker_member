# PROJECT IMPORTS
import asyncio

from heimdall_client import Heimdall, HeimdallStatusResponses
import pytest_steps
import pytest
from unittest.mock import patch, MagicMock

from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from func.src.domain.models.jwt.response import Jwt

dummy_jwt = MagicMock()


@patch.object(
    Heimdall,
    "decode_payload",
    return_value=(dummy_jwt, HeimdallStatusResponses.SUCCESS),
)
@pytest_steps.test_steps("decode_success", "get_unique_id")
def test_jwt(mocked_decoder):
    jwt = Jwt(dummy_jwt)
    asyncio.run(jwt())
    yield

    unique_id = jwt.get_unique_id_from_jwt_payload()
    assert unique_id == dummy_jwt.get.return_value.get.return_value.get.return_value
    yield


@patch.object(Heimdall, "decode_payload", return_value=(None, -1))
def test_jwt_decode_error(mocked_decoder):
    jwt = Jwt(dummy_jwt)
    with pytest.raises(ErrorOnDecodeJwt):
        asyncio.run(jwt())
