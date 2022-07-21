import asyncio
from src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import SendToPersephone
from src.transport.onboarding_steps_br import ValidateOnboardingStepsBR
from src.transport.onboarding_steps_us import ValidateOnboardingStepsUS


class UpdateBrokerMember:

    @classmethod
    def __extract_unique_id(cls, jwt_data: dict):
        unique_id = jwt_data.get("x-thebes-answer").get("user").get("unique_id")
        exchange_member = jwt_data.get("exchange_member")
        return unique_id, exchange_member

    @classmethod
    async def update_exchange_member_us(cls, jwt_data: dict, thebes_answer: str) -> bool:
        unique_id, exchange_member = cls.__extract_unique_id(jwt_data=jwt_data)

        br_step_validator = ValidateOnboardingStepsBR.onboarding_br_step_validator(thebes_answer=thebes_answer)

        us_step_validator = ValidateOnboardingStepsUS.onboarding_us_step_validator(thebes_answer=thebes_answer)

        await asyncio.gather(br_step_validator, us_step_validator)

        await SendToPersephone.register_user_exchange_member_log(
            unique_id=unique_id, exchange_member=exchange_member
        )

        was_updated = await UserRepository.update_one(
            old={"unique_id": unique_id},
            new={
                "external_exchange_requirements.us.is_exchange_member": exchange_member
            },
        )

        if not was_updated:
            raise UniqueIdWasNotUpdate

        return was_updated
