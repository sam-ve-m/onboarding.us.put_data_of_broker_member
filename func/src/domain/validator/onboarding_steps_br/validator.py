from src.domain.models.jwt.response import Jwt


class OnboardingStepsUsValidator:

    @classmethod
    async def __get_current_step(cls, jwt: Jwt):
        step_response = cls.__get_onboarding_steps_br()
        response = step_response["result"]["current_step"]

    @classmethod
    async def onboarding_br_step_validator(cls, thebes_answer: str):

        step_is_valid = response in cls.expected_step_br

        if not step_is_valid:
            raise InvalidBrOnboardingStep