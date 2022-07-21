import asyncio

from decouple import config
from starlette import status

from src.domain.enums.persephone_queue.enum import PersephoneQueue
from src.domain.exceptions.exceptions import InternalServerError, UniqueIdWasNotUpdate
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import SendToPersephone


class UserService:

    @classmethod
    def __extract_unique_id(cls, jwt_data: dict):
        unique_id = jwt_data.get("x-thebes-answer").get("user").get("unique_id")
        exchange_member = jwt_data.get("exchange_member")
        return unique_id, exchange_member

    @staticmethod
    async def update_exchange_member_us(cls, jwt_data: dict, thebes_answer: str) -> dict:
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
