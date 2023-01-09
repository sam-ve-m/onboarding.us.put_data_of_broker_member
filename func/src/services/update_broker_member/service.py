import asyncio

from func.src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from func.src.domain.models.broker_member.base.model import ExchangeMemberRequest
from func.src.domain.models.device_info.model import DeviceInfo
from func.src.domain.models.jwt.response import Jwt
from func.src.repositories.user.repository import UserRepository
from func.src.transport.onboarding_steps_br.onboarding_steps_br import (
    ValidateOnboardingStepsBr,
)
from func.src.transport.onboarding_steps_us.onboarding_steps_us import (
    ValidateOnboardingStepsUS,
)
from func.src.transport.persephone.service import SendToPersephone


class UpdateExchangeMember:
    @classmethod
    async def update_exchange_member_us(
        cls,
        jwt_data: Jwt,
        exchange_member_request: ExchangeMemberRequest,
        device_info: DeviceInfo,
    ) -> bool:
        br_step_validator = ValidateOnboardingStepsBr.validate_onboarding_steps_br(
            jwt_data=jwt_data
        )
        us_step_validator = ValidateOnboardingStepsUS.validate_onboarding_steps_us(
            jwt_data=jwt_data
        )
        await asyncio.gather(br_step_validator, us_step_validator)
        await SendToPersephone.register_user_exchange_member_log(
            jwt_data=jwt_data,
            exchange_member_request=exchange_member_request,
            device_info=device_info,
        )

        was_updated = await UserRepository.update_user_and_broker_member(
            exchange_member_request=exchange_member_request.exchange_member,
            unique_id=jwt_data.get_unique_id_from_jwt_payload(),
        )
        if not was_updated:
            raise UniqueIdWasNotUpdate()
        return was_updated
