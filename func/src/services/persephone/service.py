# THIRD PARTY IMPORTS
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.models.time_experience.model import TimeExperienceTemplates
from src.domain.enums.persephone_queue.enum import PersephoneQueue
from src.domain.exceptions.exceptions import NotSentToPersephone


class SendToPersephone:

    @classmethod
    async def register_user_time_experience_log(cls, unique_id: str, time_experience: str):

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_TRADE_TIME_EXPERIENCE_IN_US.value,
            message=TimeExperienceTemplates.user_time_experience_schema_template(
                time_experience=time_experience,
                unique_id=unique_id,
            ),
            schema_name="user_time_experience_us_schema",
        )
        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_time_experience_log::Error on trying to register log")
            raise NotSentToPersephone
