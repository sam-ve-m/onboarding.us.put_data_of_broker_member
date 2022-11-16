class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id,"
        " jwt not decoded successfully"
    )


class TransportOnboardingError(Exception):
    msg = "Jormungandr-Onboarding::ValidateOnboardingSteps::error on fetching data from fission steps"


class UserWasNotFound(Exception):
    msg = "Jormungandr-Onboarding::UserRepository::update_user_and_broker_member - user was not found"


class InvalidOnboardingStep(Exception):
    msg = "ValidateOnboardingSteps.onboarding_step_validator::you're not in this step"


class NotSentToPersephone(Exception):
    msg = "UpdateMarketTimeExperience.update_market_time_experience::sent_to_persephone:: the data was not sent to persephone"


class UniqueIdWasNotUpdate(Exception):
    msg = "UpdateMarketTimeExperience.update_market_time_experience::was_updated:: The user was not updated"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
