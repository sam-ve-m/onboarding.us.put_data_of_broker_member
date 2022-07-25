# STANDARD IMPORTS
from http import HTTPStatus
import requests

# THIRD PART IMPORTS
from decouple import config
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.response.model import ResponseModel
from src.domain.validator.onboarding_steps_us.validator import OnboardingStepsUsValidator


class ValidateOnboardingStepsUS:
    onboarding_steps_us_url = config("US_BASE_URL")


    @classmethod
    def __get_onboarding_steps_us(cls, thebes_answer: str):
        headers = {'x-thebes-answer': "{}".format(thebes_answer)}
        try:
            steps_us_response = requests.get(cls.onboarding_steps_us_url, headers=headers)
            step_response = steps_us_response.json().dict()

            step_is_valid = OnboardingStepsUsValidator.onboarding_us_step_validator(
                step_response=step_response
            )

            return step_is_valid

        except requests.exceptions.ConnectionError as error:
            Gladsheim.error(error=error)
            response = ResponseModel(
                result=False,
                success=False,
                code=InternalCode.HTTP_CONNECTION_POLL,
                message="Error On HTTP Request"
            ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return response
