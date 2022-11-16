# THIRD PARTY IMPORTS
from unittest.mock import MagicMock, patch

import pytest
from decouple import AutoConfig
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.enums.persephone_queue.enum import PersephoneQueue
from src.domain.exceptions.exceptions import NotSentToPersephone
from src.domain.models.broker_member.base.model import ExchangeMemberToPersephone
from src.transport.persephone.service import SendToPersephone

stub_jwt_data = MagicMock()
stub_exchange_member_request = MagicMock()


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone")
@patch.object(AutoConfig, "__call__")
@patch.object(ExchangeMemberToPersephone, "exchange_member_schema")
@patch.object(Gladsheim, "error")
async def test_register_user_exchange_member_log(
    mocked_logger, mocked_model, mocked_env, mocked_transp
):
    mocked_transp.return_value = True, None
    await SendToPersephone.register_user_exchange_member_log(
        stub_jwt_data, stub_exchange_member_request
    )
    mocked_transp.assert_called_once_with(
        topic=mocked_env.return_value,
        partition=PersephoneQueue.USER_EXCHANGE_MEMBER_IN_US.value,
        message=mocked_model.return_value,
        schema_name="user_exchange_member_us_schema",
    )
    mocked_model.assert_called_once_with(
        exchange_member=stub_exchange_member_request.exchange_member,
        unique_id=stub_jwt_data.get_unique_id_from_jwt_payload.return_value,
    )
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone")
@patch.object(AutoConfig, "__call__")
@patch.object(ExchangeMemberToPersephone, "exchange_member_schema")
@patch.object(Gladsheim, "error")
async def test_register_user_exchange_member_log_rasing(
    mocked_logger, mocked_model, mocked_env, mocked_transp
):
    mocked_transp.return_value = False, None
    with pytest.raises(NotSentToPersephone):
        await SendToPersephone.register_user_exchange_member_log(
            stub_jwt_data, stub_exchange_member_request
        )
    mocked_transp.assert_called_once_with(
        topic=mocked_env.return_value,
        partition=PersephoneQueue.USER_EXCHANGE_MEMBER_IN_US.value,
        message=mocked_model.return_value,
        schema_name="user_exchange_member_us_schema",
    )
    mocked_model.assert_called_once_with(
        exchange_member=stub_exchange_member_request.exchange_member,
        unique_id=stub_jwt_data.get_unique_id_from_jwt_payload.return_value,
    )
    mocked_logger.assert_called_once_with(
        message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log"
    )
