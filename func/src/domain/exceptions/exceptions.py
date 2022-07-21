class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id," \
          " jwt not decoded successfully"


class InvalidBrOnboardingStep(Exception):
    msg = "ValidateOnboardingStepsBR.onboarding_br_step_validator::you're not in this step"


class InvalidUsOnboardingStep(Exception):
    msg = "ValidateOnboardingStepsUS.onboarding_us_step_validator::you're not in this step"


class ErrorOnGettingDataFromStepsBr(Exception):
    msg = "ValidateOnboardingStepsBR.get_onboarding_steps_br::error_getting_http_response_from_fission"


class ErrorOnGettingDataFromStepsUs(Exception):
    msg = "ValidateOnboardingStepsUS.get_onboarding_steps_us::error_getting_http_response_from_fission"


class NotSentToPersephone(Exception):
    msg = "UpdateMarketTimeExperience.update_market_time_experience::sent_to_persephone:: the data was not sent to persephone"


class UniqueIdWasNotUpdate(Exception):
    msg = "UpdateMarketTimeExperience.update_market_time_experience::was_updated:: The user was not updated"


class InvalidParams(Exception):
    msg = "Jormungandr-Onboarding::w8_confirmation_param::Invalid params were sent"


class InternalServerError(Exception):
    pass
