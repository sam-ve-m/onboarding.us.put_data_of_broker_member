# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from persephone_client import Persephone
from func.src.services.persephone.service import SendToPersephone


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
async def test_register_user_exchange_member_log_when_sending_right_params_then_return_the_expected(
        mock_send_to_persephone
):
    response = await SendToPersephone.register_user_exchange_member_log(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
        exchange_member=True
    )
    assert response is None


@pytest.mark.asyncio
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
async def test_register_user_exchange_member_log_when_mocking_false_then_raise_the_expected_error(
        mock_send_to_persephone
):
    with pytest.raises(Exception):
        await SendToPersephone.register_user_exchange_member_log(
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
            exchange_member=True)
