# STANDARD IMPORTS
from unittest.mock import patch
import pytest
from flask import Flask
from werkzeug.datastructures import Headers

from main import update_exchange_member
from src.services.jwt_service.service import JWTService
from src.services.update_broker_member.service import UpdateExchangeMember

# STUB IMPORTS
from tests.src.services.jwt_service.stub_service import decoded_jwt_stub
from tests.src.main_stub import request_body_stub


@pytest.mark.asyncio
@patch.object(JWTService, "decode_jwt_from_request", return_value=decoded_jwt_stub)
@patch.object(UpdateExchangeMember, "update_exchange_member_us", return_value=True)
async def test_when_sending_right_params_to_update_exchange_member_time_then_return_the_expected(
        mock_decode_jwt_from_request,
        mock_update_exchange_member_us
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
@patch.object(JWTService, "decode_jwt_from_request", return_value=decoded_jwt_stub)
@patch.object(UpdateExchangeMember, "update_exchange_member_us", return_value=True)
async def test_when_sending_right_params_to_update_exchange_member_time_then_return_the_expected(
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
