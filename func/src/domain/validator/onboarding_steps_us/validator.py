# PROJECT IMPORTS
from src.domain.exceptions.exceptions import InvalidUsOnboardingStep


class OnboardingStepsUsValidator:

    expected_step_us = {'is_exchange_member_step', 'finished'}

    @classmethod
    async def onboarding_us_step_validator(cls, step_response: dict):
        response = step_response["result"]["current_step"]
        step_is_valid = response in cls.expected_step_us

        if not step_is_valid:
            raise InvalidUsOnboardingStep
