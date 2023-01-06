from unittest.mock import MagicMock

import pytest

from func.src.domain.exceptions.exceptions import InvalidOnboardingStep
from func.src.domain.validator.onboarding_steps_br.validator import (
    OnboardingStepsBrValidator,
)

dummy_correct_step = "correct_step"
stub_step_response = MagicMock()
dummy_wrong_step = "wrong_step"


@pytest.mark.asyncio
async def test_onboarding_br_step_validator(monkeypatch):
    monkeypatch.setattr(
        OnboardingStepsBrValidator, "expected_step_br", dummy_correct_step
    )
    stub_step_response.get.return_value.get.return_value = dummy_correct_step
    response = await OnboardingStepsBrValidator.onboarding_br_step_validator(
        stub_step_response
    )
    assert response is True


@pytest.mark.asyncio
async def test_onboarding_br_step_validator_wrong(monkeypatch):
    monkeypatch.setattr(
        OnboardingStepsBrValidator, "expected_step_br", dummy_correct_step
    )
    stub_step_response.get.return_value.get.return_value = dummy_wrong_step
    with pytest.raises(InvalidOnboardingStep):
        await OnboardingStepsBrValidator.onboarding_br_step_validator(
            stub_step_response
        )
