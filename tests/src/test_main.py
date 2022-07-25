# STANDARD IMPORTS
from unittest.mock import patch
import pytest
from flask import Flask
from heimdall_client import Heimdall, HeimdallStatusResponses
from werkzeug.datastructures import Headers

from main import update_exchange_member
from src.services.update_broker_member.service import UpdateExchangeMember

# STUB IMPORTS
from tests.src.stub_service import decoded_jwt_stub
from tests.src.main_stub import request_body_stub


@pytest.mark.asyncio
@patch.object(UpdateExchangeMember, "update_exchange_member_us", return_value=True)
@patch.object(Heimdall, "decode_payload", return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS))
async def test_when_sending_right_params_to_update_exchange_member_time_then_return_the_expected(
        mock_decode_jwt_from_request,
        mock_decode_payload
):
    app = Flask(__name__)
    with app.test_request_context(
            json=request_body_stub,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await update_exchange_member(
            request_body=request
        )
        assert response.status_code == 200


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(None, HeimdallStatusResponses.INVALID_TOKEN))
@patch.object(UpdateExchangeMember, "update_exchange_member_us", return_value=True)
async def test_when_sending_invalid_jwt_to_update_exchange_member_time_then_raise_error(
        mock_decode_jwt_from_request,
        mock_update_exchange_member_us
):
    app = Flask(__name__)
    with app.test_request_context(
            json=None,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        with pytest.raises(Exception):
            await update_exchange_member(
                request_body=None
            )
