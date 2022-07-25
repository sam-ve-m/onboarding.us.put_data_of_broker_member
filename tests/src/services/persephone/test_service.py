# STANDARD IMPORTS
from unittest.mock import patch, Mock
import pytest

# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses
from persephone_client import Persephone
from src.domain.models.broker_member.base.model import ExchangeMemberRequest
from func.src.services.persephone.service import SendToPersephone

# STUB IMPORTS
from tests.src.stub_service import decoded_jwt_stub

get_unique_id_from_jwt_payload = "125458.hagfsdsa"


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(Heimdall, "decode_payload", return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS))
async def test_register_user_exchange_member_log_when_sending_right_params_then_return_the_expected(
        mock_send_to_persephone, mock_decode_payload
):
    response = await SendToPersephone.register_user_exchange_member_log(
        jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
        exchange_member_request=ExchangeMemberRequest(**{"exchange_member": True})
    )
    assert response is None


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
async def test_register_user_exchange_member_log_when_mocking_false_then_raise_the_expected_error(
        mock_send_to_persephone
):
    with pytest.raises(Exception):
        await SendToPersephone.register_user_exchange_member_log(
            jwt_data=None,
            exchange_member_request=None)
