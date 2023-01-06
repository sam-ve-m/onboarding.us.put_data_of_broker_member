from unittest.mock import patch, AsyncMock, MagicMock

import aiohttp
import pytest
from decouple import AutoConfig
from etria_logger import Gladsheim

from func.src.domain.exceptions.exceptions import (
    TransportOnboardingError,
    InvalidOnboardingStep,
)
from func.src.domain.validator.onboarding_steps_us.validator import (
    OnboardingStepsUsValidator,
)

dummy_env = "dummy env"

with patch.object(AutoConfig, "__call__", return_value=dummy_env):
    from func.src.transport.onboarding_steps_us.onboarding_steps_us import (
        ValidateOnboardingStepsUS,
    )


fake_response = AsyncMock()
fake_session = AsyncMock()
fake_session.get = MagicMock()
fake_session.get.return_value = AsyncMock()
fake_session.get.return_value.__aenter__.return_value = fake_response

dummy_jwt = "jwt"
stub_jwt_data = MagicMock()
dummy_header = {"x-thebes-answer": dummy_jwt}
stub_jwt_data.get_jwt.return_value = dummy_jwt


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "__init__", return_value=None)
@patch.object(aiohttp.ClientSession, "__aenter__", return_value=fake_session)
@patch.object(aiohttp.ClientSession, "__aexit__")
@patch.object(OnboardingStepsUsValidator, "onboarding_us_step_validator")
@patch.object(Gladsheim, "error")
async def test_validate_onboarding_steps_us(
    mocked_logger,
    mocked_validator,
    mocked_async_exit,
    mocked_async_enter,
    mocked_instance,
):
    response = await ValidateOnboardingStepsUS.validate_onboarding_steps_us(
        stub_jwt_data
    )
    fake_session.get.assert_called_once_with(dummy_env, headers=dummy_header)
    mocked_validator.assert_called_once_with(
        step_response=fake_response.json.return_value
    )
    assert response == mocked_validator.return_value
    mocked_logger.assert_not_called()


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "__init__", return_value=None)
@patch.object(aiohttp.ClientSession, "__aenter__", return_value=fake_session)
@patch.object(aiohttp.ClientSession, "__aexit__")
@patch.object(OnboardingStepsUsValidator, "onboarding_us_step_validator")
@patch.object(Gladsheim, "error")
async def test_validate_onboarding_steps_us_wrong_step(
    mocked_logger,
    mocked_validator,
    mocked_async_exit,
    mocked_async_enter,
    mocked_instance,
):
    wrong_step_exception = InvalidOnboardingStep()
    mocked_instance.side_effect = wrong_step_exception
    with pytest.raises(InvalidOnboardingStep):
        await ValidateOnboardingStepsUS.validate_onboarding_steps_us(stub_jwt_data)
    mocked_logger.assert_called_once_with(
        error=wrong_step_exception, message="User in invalid step"
    )


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "__init__", return_value=None)
@patch.object(aiohttp.ClientSession, "__aenter__", return_value=fake_session)
@patch.object(aiohttp.ClientSession, "__aexit__")
@patch.object(OnboardingStepsUsValidator, "onboarding_us_step_validator")
@patch.object(Gladsheim, "error")
async def test_validate_onboarding_steps_us_other_error(
    mocked_logger,
    mocked_validator,
    mocked_async_exit,
    mocked_async_enter,
    mocked_instance,
):
    other_exception = Exception()
    mocked_instance.side_effect = other_exception
    with pytest.raises(TransportOnboardingError):
        await ValidateOnboardingStepsUS.validate_onboarding_steps_us(stub_jwt_data)
    mocked_logger.assert_called_once_with(error=other_exception)
