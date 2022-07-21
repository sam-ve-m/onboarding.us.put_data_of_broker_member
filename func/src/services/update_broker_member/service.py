import asyncio


class UserService:

    @staticmethod
    async def update_exchange_member_us(
        payload: dict
    ) -> dict:
        thebes_answer = payload["x-thebes-answer"]
        thebes_answer_user = thebes_answer["user"]
        user_is_exchange_member = payload["is_exchange_member"]
        br_step_validator = UserService.onboarding_br_step_validator(
            payload=payload, onboard_step=["finished"]
        )
        us_step_validator = UserService.onboarding_us_step_validator(
            payload=payload, onboard_step=["is_exchange_member_step"]
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_EXCHANGE_MEMBER_IN_US.value,
            message=get_user_exchange_member_schema_template_with_data(
                exchange_member=user_is_exchange_member,
                unique_id=thebes_answer["user"]["unique_id"],
            ),
            schema_name="user_exchange_member_us_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        was_updated = await UserRepository.update_one(
            old={"unique_id": thebes_answer_user["unique_id"]},
            new={
                "external_exchange_requirements.us.is_exchange_member": user_is_exchange_member
            },
        )
        if not was_updated:
            raise InternalServerError("common.unable_to_process")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }