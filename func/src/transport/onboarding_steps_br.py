# STANDARD IMPORTS
from http import HTTPStatus
import requests

# THIRD PART IMPORTS
# from decouple import config
from etria_logger import Gladsheim
from src.infrastructure.env_config import config

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import InvalidBrOnboardingStep, ErrorOnGettingDataFromStepsBr
from src.domain.response.model import ResponseModel


class ValidateOnboardingStepsBR:
    onboarding_steps_br_url = config("BR_BASE_URL")
    expected_step_br = "finished"

    @classmethod
    def __get_onboarding_steps_br(cls, thebes_answer: str):
        # headers = {'x-thebes-answer': "{}".format(thebes_answer)}
        try:
            # Todo - Fission route not yet deployed to access by http requests
            # steps_br_response = requests.get(cls.onboarding_steps_br_url, headers=headers)

            response = {'terms': True,
                        'user_document_validator': True,
                        'politically_exposed': True,
                        'exchange_member': True,
                        'company_director': True,
                        'external_fiscal_tax_confirmation': True,
                        'employ': True,
                        'time_experience': True,
                        'current_step': 'finished'}
            return response

        except ErrorOnGettingDataFromStepsBr as error:
            Gladsheim.error(error=error)
            response = ResponseModel(
                result=False,
                success=False,
                code=InternalCode.HTTP_CONNECTION_POLL,
                message="Error On HTTP Request"
            ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return response

    @classmethod
    async def onboarding_br_step_validator(cls, thebes_answer: str):
        response = cls.__get_onboarding_steps_br(thebes_answer=thebes_answer)
        current_step = response.get("current_step")

        if not current_step == cls.expected_step_br:
            raise InvalidBrOnboardingStep
