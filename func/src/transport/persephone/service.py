from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

from func.src.domain.enums.persephone_queue.enum import PersephoneQueue
from func.src.domain.exceptions.exceptions import NotSentToPersephone
from func.src.domain.models.broker_member.base.model import (
    ExchangeMemberToPersephone,
    ExchangeMemberRequest,
)
from func.src.domain.models.device_info.model import DeviceInfo
from func.src.domain.models.jwt.response import Jwt


class SendToPersephone:
    @classmethod
    async def register_user_exchange_member_log(
        cls,
        jwt_data: Jwt,
        exchange_member_request: ExchangeMemberRequest,
        device_info: DeviceInfo,
    ):

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_EXCHANGE_MEMBER_IN_US.value,
            message=ExchangeMemberToPersephone.exchange_member_schema(
                exchange_member=exchange_member_request.exchange_member,
                unique_id=jwt_data.get_unique_id_from_jwt_payload(),
                device_info=device_info,
            ),
            schema_name="user_exchange_member_us_schema",
        )
        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log"
            )
            raise NotSentToPersephone()
