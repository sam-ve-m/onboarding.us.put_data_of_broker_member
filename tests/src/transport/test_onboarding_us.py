# # STANDARD IMPORTS
# from unittest.mock import patch
# import pytest
#
# # PROJECT IMPORTS
# from src.domain.exceptions.exceptions import InvalidUsOnboardingStep
# from src.transport.onboarding_steps_us.onboarding_steps_us import ValidateOnboardingStepsUS
# from tests.src.transport.stub_onboarding import us_steps_result_stub
# from stub_service import jwt_to_decode_stub
#
#
# @pytest.mark.asyncio
# @patch.object(
#     ValidateOnboardingStepsUS,
#     "_ValidateOnboardingStepsUS__get_onboarding_steps_us",
#     return_value=us_steps_result_stub)
# async def test_when_sending_right_params_to_onboarding_us_step_validator_then_return_the_expected(
#         mock_get_onboarding_steps_br
# ):
#     response = await ValidateOnboardingStepsUS.onboarding_us_step_validator(
#         thebes_answer=jwt_to_decode_stub
#     )
#     assert response is None
#
#
# @pytest.mark.asyncio
# @patch.object(
#     ValidateOnboardingStepsUS,
#     "_ValidateOnboardingStepsUS__get_onboarding_steps_us",
#     return_value="current_step")
# async def test_when_sending_wrong_params_to_onboarding_us_step_validator_then_raise_error(
#         mock_get_onboarding_steps_us
# ):
#     with pytest.raises(InvalidUsOnboardingStep):
#         await ValidateOnboardingStepsUS.onboarding_us_step_validator(
#             thebes_answer=None
#         )
