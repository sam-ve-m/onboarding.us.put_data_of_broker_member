# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses
from func.src.services.jwt_service.service import JWTService
from tests.src.services.jwt_service.stub_service import (
                                                            jwt_to_decode_stub,
                                                            decoded_jwt_stub,
                                                            jwt_data_stub,
                                                            jwt_invalid
                                                        )


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(jwt_data_stub, HeimdallStatusResponses.SUCCESS))
async def test_when_sending_right_params_to_the_function_then_return_the_expected(
        mock_decode_payload
):
    response = await JWTService.decode_jwt_from_request(
        jwt_data=jwt_to_decode_stub
    )
    assert response == decoded_jwt_stub


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(jwt_invalid, HeimdallStatusResponses.INVALID_TOKEN))
async def test_when_sending_wrong_params_to_decode_jwt_from_request_then_raise_error(
        mock_decode_payload
):
    with pytest.raises(Exception):
        await JWTService.decode_jwt_from_request(
            jwt_data=""
        )
