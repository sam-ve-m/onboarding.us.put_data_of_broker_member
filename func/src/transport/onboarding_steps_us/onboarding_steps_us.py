# STANDARD IMPORTS
import aiohttp

# THIRD PART IMPORTS
from decouple import config
from etria_logger import Gladsheim

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import (
    TransportOnboardingError,
    InvalidOnboardingStep,
)
from func.src.domain.models.jwt.response import Jwt
from func.src.domain.validator.onboarding_steps_us.validator import (
    OnboardingStepsUsValidator,
)


class ValidateOnboardingStepsUS:
    steps_us_url = config("US_BASE_URL")

    @classmethod
    async def validate_onboarding_steps_us(cls, jwt_data: Jwt):
        headers = {"x-thebes-answer": "{}".format(jwt_data.get_jwt())}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(cls.steps_us_url, headers=headers) as response:
                    step_response = await response.json()

                    step_is_valid = (
                        await OnboardingStepsUsValidator.onboarding_us_step_validator(
                            step_response=step_response
                        )
                    )

                    return step_is_valid

        except InvalidOnboardingStep as error:
            Gladsheim.error(error=error, message="User in invalid step")
            raise error

        except Exception as error:
            Gladsheim.error(error=error)
            raise TransportOnboardingError()
