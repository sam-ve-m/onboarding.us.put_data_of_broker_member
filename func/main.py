from http import HTTPStatus

import flask
from etria_logger import Gladsheim

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import (
    InvalidOnboardingStep,
    ErrorOnDecodeJwt,
    NotSentToPersephone,
    UniqueIdWasNotUpdate,
    TransportOnboardingError,
    UserWasNotFound,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.models.broker_member.base.model import ExchangeMemberRequest
from func.src.domain.models.jwt.response import Jwt
from func.src.domain.models.response.model import ResponseModel
from func.src.services.update_broker_member.service import UpdateExchangeMember
from func.src.transport.device_info.transport import DeviceSecurity


async def update_exchange_member() -> flask.Response:
    try:
        x_thebes_answer = flask.request.headers.get("x-thebes-answer")
        x_device_info = flask.request.headers.get("x-device-info")
        request_body = flask.request.json

        jwt_data = Jwt(jwt=x_thebes_answer)
        await jwt_data()
        device_info = await DeviceSecurity.get_device_info(x_device_info)
        exchange_member = ExchangeMemberRequest(**request_body)

        service_response = await UpdateExchangeMember.update_exchange_member_us(
            jwt_data=jwt_data,
            exchange_member_request=exchange_member,
            device_info=device_info,
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS.value,
            message="The Broker Member US Data Was Successfully Updated",
            result=service_response,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidOnboardingStep as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message="User in invalid onboarding step",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID.value,
            message="Error On Decoding JWT",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except NotSentToPersephone as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_SENT_TO_PERSEPHONE.value,
            message="Not Sent to Persephone",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UniqueIdWasNotUpdate as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNIQUE_ID_WAS_NOT_UPDATED.value,
            message="Unique Id Was Not Updated",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UserWasNotFound as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND.value,
            message="Unique Id Was Not Found",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except TransportOnboardingError as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.TRANSPORT_LAYER_ERROR.value,
            message="Transport Layer Error - not able to fetch data from transport response",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS.value, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
