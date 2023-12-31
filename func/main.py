from http import HTTPStatus
import flask

from etria_logger import Gladsheim

from src.domain.enums.status_code.enum import InternalCode
from src.domain.models.broker_member.base.model import ExchangeMemberRequest
from src.domain.models.jwt.response import Jwt
from src.domain.models.response.model import ResponseModel
from src.services.update_broker_member.service import UpdateExchangeMember
from src.domain.exceptions.exceptions import (
    InvalidOnboardingStep,
    ErrorOnDecodeJwt,
    NotSentToPersephone,
    UniqueIdWasNotUpdate,
    TransportOnboardingError,
    UserWasNotFound,
)


async def update_exchange_member() -> flask.Response:
    thebes_answer = flask.request.headers.get("x-thebes-answer")

    try:
        jwt_data = Jwt(jwt=thebes_answer)
        await jwt_data()
        exchange_member = ExchangeMemberRequest(**flask.request.json)

        service_response = await UpdateExchangeMember.update_exchange_member_us(
            jwt_data=jwt_data,
            exchange_member_request=exchange_member
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS.value,
            message="The Broker Member US Data Was Successfully Updated",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidOnboardingStep as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_ONBOARDING_STEP.value,
            message="User in invalid onboarding step"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID.value,
            message="Error On Decoding JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except NotSentToPersephone as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_SENT_TO_PERSEPHONE.value,
            message="Not Sent to Persephone"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UniqueIdWasNotUpdate as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNIQUE_ID_WAS_NOT_UPDATED.value,
            message="Unique Id Was Not Updated"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserWasNotFound as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND.value,
            message="Unique Id Was Not Found"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except TransportOnboardingError as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.TRANSPORT_LAYER_ERROR.value,
            message="Transport Layer Error - not able to fetch data from transport response"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
