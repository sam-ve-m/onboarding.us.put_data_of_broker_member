import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config

from func.src.transport.device_info.transport import DeviceSecurity

dummy_env = "dummy env"

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__", return_value=dummy_env):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from func.main import update_exchange_member
                from func.src.domain.models.jwt.response import Jwt
                from func.src.domain.exceptions.exceptions import *
                from func.src.domain.enums.status_code.enum import InternalCode
                from func.src.domain.models.response.model import ResponseModel
                from func.src.services.update_broker_member.service import (
                    UpdateExchangeMember,
                )
                from func.src.domain.models.broker_member.base.model import (
                    ExchangeMemberRequest,
                )


invalid_onboarding_step_case = (
    InvalidOnboardingStep(),
    InvalidOnboardingStep.msg,
    InternalCode.INVALID_PARAMS,
    "User in invalid onboarding step",
    HTTPStatus.UNAUTHORIZED,
)
error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Error On Decoding JWT",
    HTTPStatus.UNAUTHORIZED,
)
not_sent_to_persephone_case = (
    NotSentToPersephone(),
    NotSentToPersephone.msg,
    InternalCode.NOT_SENT_TO_PERSEPHONE,
    "Not Sent to Persephone",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
unique_id_was_not_update_case = (
    UniqueIdWasNotUpdate(),
    UniqueIdWasNotUpdate.msg,
    InternalCode.UNIQUE_ID_WAS_NOT_UPDATED,
    "Unique Id Was Not Updated",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
user_was_not_found_case = (
    UserWasNotFound(),
    UserWasNotFound.msg,
    InternalCode.USER_WAS_NOT_FOUND,
    "Unique Id Was Not Found",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
transport_onboarding_error_case = (
    TransportOnboardingError(),
    TransportOnboardingError.msg,
    InternalCode.TRANSPORT_LAYER_ERROR,
    "Transport Layer Error - not able to fetch data from transport response",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
validation_error_case = (
    ValueError,
    "Invalid parameters",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Invalid parameters",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
device_info_request_case = (
    DeviceInfoRequestFailed(),
    "Error trying to get device info",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Error trying to get device info",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
no_device_info_case = (
    DeviceInfoNotSupplied(),
    "Device info not supplied",
    InternalCode.INVALID_PARAMS,
    "Device info not supplied",
    HTTPStatus.BAD_REQUEST,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception,error_message,internal_status_code,response_message,response_status_code",
    [
        invalid_onboarding_step_case,
        error_on_decode_jwt_case,
        not_sent_to_persephone_case,
        unique_id_was_not_update_case,
        user_was_not_found_case,
        transport_onboarding_error_case,
        exception_case,
        device_info_request_case,
        no_device_info_case,
    ],
)
@patch.object(UpdateExchangeMember, "update_exchange_member_us")
@patch.object(ExchangeMemberRequest, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_exchange_member_raising_errors(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_jwt_decode,
    mocked_jwt_instance,
    mocked_logger,
    mocked_model,
    mocked_service,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await update_exchange_member()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code.value, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(
    UpdateExchangeMember, "update_exchange_member_us", return_value=dummy_response
)
@patch.object(ExchangeMemberRequest, "__init__", return_value=None)
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_exchange_member(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_jwt_decode,
    mocked_jwt_instance,
    mocked_logger,
    mocked_model,
    mocked_service,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await update_exchange_member()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=True,
        code=InternalCode.SUCCESS.value,
        message="The Broker Member US Data Was Successfully Updated",
        result=dummy_response,
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
