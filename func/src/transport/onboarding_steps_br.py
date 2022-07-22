# STANDARD IMPORTS
from http import HTTPStatus
import requests

# THIRD PART IMPORTS
from decouple import config
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import InvalidBrOnboardingStep
from src.domain.response.model import ResponseModel


class ValidateOnboardingStepsBR:
    onboarding_steps_br_url = config("BR_BASE_URL")
    expected_step_br = "finished"

    @classmethod
    def __get_onboarding_steps_br(cls, thebes_answer: str):
        headers = {'x-thebes-answer': "{}".format(thebes_answer)}
        try:
            steps_br_response = requests.get(cls.onboarding_steps_br_url, headers=headers)
            step_response = steps_br_response.json()
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
    async def onboarding_br_step_validator(cls, thebes_answer: str):
        response = cls.__get_onboarding_steps_br(thebes_answer=thebes_answer)
        step_is_valid = response in cls.expected_step_br

        if not step_is_valid:
            raise InvalidBrOnboardingStep
