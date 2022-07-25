# STANDARD IMPORTS
import asyncio

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from src.domain.models.broker_member.base.model import ExchangeMemberRequest
from src.domain.models.jwt.response import Jwt
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import SendToPersephone
from src.transport.onboarding_steps_br.onboarding_steps_br import ValidateOnboardingStepsBr
from src.transport.onboarding_steps_us.onboarding_steps_us import ValidateOnboardingStepsUS


class UpdateExchangeMember:

    @classmethod
    async def update_exchange_member_us(
            cls,
            jwt_data: Jwt,
            exchange_member_request: ExchangeMemberRequest) -> bool:

        br_step_validator = ValidateOnboardingStepsBr.validate_onboarding_steps_br(jwt_data=jwt_data)

        us_step_validator = ValidateOnboardingStepsUS.validate_onboarding_steps_us(jwt_data=jwt_data)

        await asyncio.gather(br_step_validator, us_step_validator)

        await SendToPersephone.register_user_exchange_member_log(
            jwt_data=jwt_data,
            exchange_member_request=exchange_member_request
        )

        was_updated = await UserRepository.update_user_and_exchange_member(
            jwt_data=jwt_data
            )

        if not was_updated:
            raise UniqueIdWasNotUpdate

        return was_updated
