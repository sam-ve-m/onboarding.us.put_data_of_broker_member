# STANDARD IMPORTS
from unittest.mock import patch, AsyncMock
import pytest

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from src.repositories.user.repository import UserRepository
from src.services.persephone.service import SendToPersephone
from src.services.update_broker_member.service import UpdateExchangeMember
from src.transport.onboarding_steps_br import ValidateOnboardingStepsBR
from src.transport.onboarding_steps_us import ValidateOnboardingStepsUS

# STUB IMPORTS
from tests.src.services.jwt_service.stub_service import decoded_jwt_stub, jwt_to_decode_stub


@pytest.mark.asyncio
@patch.object(UpdateExchangeMember, "_UpdateExchangeMember__extract_unique_id", return_value=(
        '40db7fee-6d60-4d73-824f-1bf87edc4491', True
))
@patch.object(ValidateOnboardingStepsBR, "onboarding_br_step_validator", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "onboarding_us_step_validator", side_effect=[None, None])
@patch.object(SendToPersephone, "register_user_exchange_member_log", return_value=None)
@patch.object(UserRepository, "update_one", return_value=True)
async def test_when_sending_right_params_to_update_exchange_member_us_then_return_the_expected(
        mock_extract_unique_id,
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_exchange_member_log,
        mock_update_one
):
    response = await UpdateExchangeMember.update_exchange_member_us(
        jwt_data=decoded_jwt_stub,
        thebes_answer=jwt_to_decode_stub
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(UpdateExchangeMember, "_UpdateExchangeMember__extract_unique_id", return_value=(
        '40db7fee-6d60-4d73-824f-1bf87edc4491', True
))
@patch.object(ValidateOnboardingStepsBR, "onboarding_br_step_validator", return_value=AsyncMock())
@patch.object(ValidateOnboardingStepsUS, "onboarding_us_step_validator", return_value=AsyncMock())
@patch.object(SendToPersephone, "register_user_exchange_member_log", return_value=None)
@patch.object(UserRepository, "update_one", return_value=False)
async def test_when_sending_wrong_params_to_update_exchange_member_us_then_raise_unique_id_was_not_updated_error(
        mock_extract_unique_id,
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_time_experience_log,
        mock_update_one
):
    with pytest.raises(UniqueIdWasNotUpdate):
        await UpdateExchangeMember.update_exchange_member_us(
            jwt_data=decoded_jwt_stub,
            thebes_answer=jwt_to_decode_stub
        )
