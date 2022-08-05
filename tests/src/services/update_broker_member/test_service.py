# STANDARD IMPORTS
from unittest.mock import patch, Mock
import pytest

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import UniqueIdWasNotUpdate
from func.src.domain.models.broker_member.base.model import ExchangeMemberRequest
from func.src.repositories.user.repository import UserRepository
from func.src.services.persephone.service import SendToPersephone
from func.src.services.update_broker_member.service import UpdateExchangeMember
from func.src.transport.onboarding_steps_br.onboarding_steps_br import ValidateOnboardingStepsBr
from func.src.transport.onboarding_steps_us.onboarding_steps_us import ValidateOnboardingStepsUS


get_unique_id_from_jwt_payload = "125458.hagfsdsa"


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us", side_effect=[None, None])
@patch.object(SendToPersephone, "register_user_exchange_member_log", return_value=None)
@patch.object(UserRepository, "update_user_and_broker_member", return_value=True)
async def test_when_sending_right_params_to_update_exchange_member_us_then_return_the_expected(
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_exchange_member_log,
        mock_update_one
):
    response = await UpdateExchangeMember.update_exchange_member_us(
        jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
        exchange_member_request=ExchangeMemberRequest(**{"exchange_member": True})
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us", side_effect=[None, None])
@patch.object(SendToPersephone, "register_user_exchange_member_log", return_value=None)
@patch.object(UserRepository, "update_user_and_broker_member", return_value=False)
async def test_when_sending_wrong_params_to_update_exchange_member_us_then_raise_unique_id_was_not_updated_error(
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_time_experience_log,
        mock_update_one
):
    with pytest.raises(UniqueIdWasNotUpdate):
        await UpdateExchangeMember.update_exchange_member_us(
            jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
            exchange_member_request=ExchangeMemberRequest(**{"exchange_member": True})
        )
