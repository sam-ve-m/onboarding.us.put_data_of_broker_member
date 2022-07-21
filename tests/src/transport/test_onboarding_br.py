# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from func.src.transport.onboarding_steps_br import ValidateOnboardingStepsBR

# STUB IMPORTS
from tests.src.services.jwt_service.stub_service import jwt_to_decode_stub
from tests.src.transport.stub_onboarding import br_steps_result_stub


@pytest.mark.asyncio
@patch.object(
    ValidateOnboardingStepsBR,
    "_ValidateOnboardingStepsBR__get_onboarding_steps_br",
    return_value=br_steps_result_stub)
async def test_when_sending_right_params_to_onboarding_br_step_validator_then_return_the_expected(
        mock_get_onboarding_steps_br
):
    response = await ValidateOnboardingStepsBR.onboarding_br_step_validator(
        thebes_answer=jwt_to_decode_stub
    )
    assert response is None


@pytest.mark.asyncio
@patch.object(
    ValidateOnboardingStepsBR,
    "_ValidateOnboardingStepsBR__get_onboarding_steps_br",
    return_value=Exception)
async def test_when_sending_wrong_params_to_onboarding_br_step_validator_then_raise_error(
        mock_get_onboarding_steps_br
):
    with pytest.raises(Exception):
        await ValidateOnboardingStepsBR.onboarding_br_step_validator(
            thebes_answer=None
        )
