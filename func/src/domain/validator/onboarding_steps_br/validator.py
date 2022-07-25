# PROJECT IMPORTS
from src.domain.exceptions.exceptions import InvalidBrOnboardingStep


class OnboardingStepsBrValidator:

    expected_step_br = "finished"

    @classmethod
    def onboarding_br_step_validator(cls, step_response: dict):
        response = step_response["result"]["current_step"]

        step_is_valid = response in cls.expected_step_br

        if not step_is_valid:
            raise InvalidBrOnboardingStep
