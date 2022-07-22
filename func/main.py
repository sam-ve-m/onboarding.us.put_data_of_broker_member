# STANDARD IMPORTS
from http import HTTPStatus

import requests
from flask import request, Response, Request, Flask

# THIRD PART IMPORTS
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.models.broker_member.model import ExchangeMemberModel
from src.domain.response.model import ResponseModel
from src.services.jwt_service.service import JWTService
from src.services.update_broker_member.service import UpdateExchangeMember
from src.domain.exceptions.exceptions import (
                                        InvalidUsOnboardingStep,
                                        InvalidBrOnboardingStep,
                                        ErrorOnDecodeJwt,
                                        NotSentToPersephone,
                                        UniqueIdWasNotUpdate,
                                        InvalidParams,
                                        ErrorOnGettingDataFromStepsBr,
                                        ErrorOnGettingDataFromStepsUs
                                    )

app = Flask(__name__)


@app.route('/put/update_exchange_member')
async def update_exchange_member(request_body: Request = request) -> Response:
    thebes_answer = request_body.headers.get("x-thebes-answer")

    try:
        jwt_data = await JWTService.decode_jwt_from_request(jwt_data=thebes_answer)
        exchange_member = ExchangeMemberModel(**request_body.json).dict()
        payload = {"x-thebes-answer": jwt_data}
        payload.update(exchange_member)
        service_response = await UpdateExchangeMember.update_exchange_member_us(
            thebes_answer=thebes_answer, jwt_data=payload
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="The Broker Member US Data Was Successfully Updated",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidBrOnboardingStep as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.INVALID_BR_ONBOARDING_STEP,
            message="Invalid Onboarding Step"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error On Decoding JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except NotSentToPersephone as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.NOT_SENT_TO_PERSEPHONE,
            message="Not Sent to Persephone"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except requests.exceptions.ConnectionError as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.HTTP_CONNECTION_POLL,
            message="Error On HTTP Request"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UniqueIdWasNotUpdate as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.UNIQUE_ID_WAS_NOT_UPDATED,
            message="Unique Id Was Not Updated"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except InvalidUsOnboardingStep as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.INVALID_US_ONBOARDING_STEP,
            message="Invalid Onboarding Step"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except InvalidParams as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid Params Were Sent"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnGettingDataFromStepsBr as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.ERROR_ON_GETTING_DATA_FROM_BR_STEPS,
            message="Http Error while getting data from fission"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnGettingDataFromStepsUs as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.ERROR_ON_GETTING_DATA_FROM_US_STEPS,
            message="Http Error while getting data from fission"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

if __name__ == "__main__":
    app.run(debug=True)
