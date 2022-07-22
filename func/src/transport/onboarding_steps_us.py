# STANDARD IMPORTS
from http import HTTPStatus
import requests

# THIRD PART IMPORTS
from decouple import config
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import InvalidUsOnboardingStep
from src.domain.response.model import ResponseModel


class ValidateOnboardingStepsUS:
    onboarding_steps_us_url = config("US_BASE_URL")
    expected_step_us = {'is_exchange_member_step', 'finished'}

    @classmethod
    def __get_onboarding_steps_us(cls, thebes_answer: str):
        headers = {'x-thebes-answer': "{}".format(thebes_answer)}
        try:
            steps_us_response = requests.get(cls.onboarding_steps_us_url, headers=headers)
            step_response = steps_us_response.json()
            response = step_response["result"]["current_step"]
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

    @classmethod
    async def onboarding_us_step_validator(cls, thebes_answer: str):
        response = cls.__get_onboarding_steps_us(thebes_answer=thebes_answer)
        step_is_valid = response in cls.expected_step_us

        if not step_is_valid:
            raise InvalidUsOnboardingStep
