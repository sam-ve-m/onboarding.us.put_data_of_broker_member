# THIRD PARTY IMPORTS
# from decouple import config
from src.infrastructure.env_config import config
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.enums.persephone_queue.enum import PersephoneQueue
from src.domain.exceptions.exceptions import NotSentToPersephone
from src.domain.models.broker_member.model import ExchangeMemberTemplates


class SendToPersephone:

    @classmethod
    async def register_user_exchange_member_log(cls, unique_id: str, exchange_member: str):

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_EXCHANGE_MEMBER_IN_US.value,
            message=ExchangeMemberTemplates.exchange_member_schema_template(
                exchange_member=exchange_member,
                unique_id=unique_id,
            ),
            schema_name="prospect_user_schema",
        )
        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log")
            raise NotSentToPersephone
