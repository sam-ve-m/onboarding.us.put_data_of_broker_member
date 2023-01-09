from unittest.mock import MagicMock, patch

import pytest
from decouple import Config

from func.src.domain.models.device_info.model import DeviceInfo

with patch.object(Config, "__call__", return_value="INFO"):
    from func.src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
    from func.src.repositories.user.repository import UserRepository
    from func.src.services.update_broker_member.service import UpdateExchangeMember
    from func.src.transport.onboarding_steps_br.onboarding_steps_br import (
        ValidateOnboardingStepsBr,
    )
    from func.src.transport.onboarding_steps_us.onboarding_steps_us import (
        ValidateOnboardingStepsUS,
    )
    from func.src.transport.persephone.service import SendToPersephone

dummy_jwt_data = MagicMock()
dummy_exchange_member_request = MagicMock()
dummy_device_info = DeviceInfo({"precision": 1}, "")


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br")
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_user_and_broker_member")
async def test_update_exchange_member_us_user_not_updated(
    mocked_repo, mocked_transp, mocked_valid_br, mocked_valid_us
):
    mocked_repo.return_value = None
    with pytest.raises(UniqueIdWasNotUpdate):
        await UpdateExchangeMember.update_exchange_member_us(
            dummy_jwt_data, dummy_exchange_member_request, dummy_device_info
        )
    mocked_valid_br.assert_called_once_with(jwt_data=dummy_jwt_data)
    mocked_valid_us.assert_called_once_with(jwt_data=dummy_jwt_data)
    mocked_transp.assert_called_once_with(
        jwt_data=dummy_jwt_data,
        exchange_member_request=dummy_exchange_member_request,
        device_info=dummy_device_info,
    )
    mocked_repo.assert_called_once_with(
        exchange_member_request=dummy_exchange_member_request.exchange_member,
        unique_id=dummy_jwt_data.get_unique_id_from_jwt_payload.return_value,
    )


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br")
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_user_and_broker_member")
async def test_update_exchange_member_us(
    mocked_repo, mocked_transp, mocked_valid_br, mocked_valid_us
):
    result = await UpdateExchangeMember.update_exchange_member_us(
        dummy_jwt_data, dummy_exchange_member_request, dummy_device_info
    )
    mocked_valid_br.assert_called_once_with(jwt_data=dummy_jwt_data)
    mocked_valid_us.assert_called_once_with(jwt_data=dummy_jwt_data)
    mocked_transp.assert_called_once_with(
        jwt_data=dummy_jwt_data,
        exchange_member_request=dummy_exchange_member_request,
        device_info=dummy_device_info,
    )
    mocked_repo.assert_called_once_with(
        exchange_member_request=dummy_exchange_member_request.exchange_member,
        unique_id=dummy_jwt_data.get_unique_id_from_jwt_payload.return_value,
    )
    assert result == mocked_repo.return_value
