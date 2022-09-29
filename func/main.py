# STANDARD IMPORTS
from http import HTTPStatus
from flask import request, Response, Request

# THIRD PART IMPORTS
from etria_logger import Gladsheim

# PROJECT IMPORTS
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


async def update_exchange_member(request_body: Request = request) -> Response:
    thebes_answer = request_body.headers.get("x-thebes-answer")

    try:
        jwt_data = Jwt(jwt=thebes_answer)
        await jwt_data()
        exchange_member = ExchangeMemberRequest(**request_body.json)

        service_response = await UpdateExchangeMember.update_exchange_member_us(
            jwt_data=jwt_data,
            exchange_member_request=exchange_member
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="The Broker Member US Data Was Successfully Updated",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidOnboardingStep as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_ONBOARDING_STEP,
            message="User in invalid onboarding step"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error On Decoding JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except NotSentToPersephone as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_SENT_TO_PERSEPHONE,
            message="Not Sent to Persephone"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UniqueIdWasNotUpdate as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNIQUE_ID_WAS_NOT_UPDATED,
            message="Unique Id Was Not Updated"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserWasNotFound as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="Unique Id Was Not Found"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except TransportOnboardingError as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.TRANSPORT_LAYER_ERROR,
            message="Transport Layer Error - not able to fetch data from transport response"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
