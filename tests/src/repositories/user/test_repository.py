import pytest
from decouple import Config
from etria_logger import Gladsheim
from unittest.mock import patch, MagicMock, AsyncMock


dummy_env = "dummy env"

with patch.object(Config, "__call__", return_value=dummy_env):
    from func.src.domain.exceptions.exceptions import UserWasNotFound
    from func.src.repositories.user.repository import UserRepository

fake_infra = MagicMock()
fake_collection = AsyncMock()
dummy_unique_id = "dummy unique_id"
dummy_is_exchange_member = False
index_error = IndexError()


@patch.object(Gladsheim, "error")
async def test_update_user_and_broker_member_raising_error_in_get_collection(
    mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.side_effect = index_error
    with pytest.raises(index_error.__class__):
        await UserRepository.update_user_and_broker_member(
            dummy_unique_id, dummy_is_exchange_member
        )
    mocked_logger.assert_called_once_with(
        error=index_error,
        database=dummy_env,
        collection=dummy_env,
        message="UserRepository::__get_collection::Error when trying to get collection",
    )


dummy_update_fields = {
    "$set": {
        "external_exchange_requirements.us.is_exchange_member": dummy_is_exchange_member
    }
}
dummy_user_filter = {"unique_id": dummy_unique_id}
dummy_fiscal_tax_residence = "fiscal_tax_residence"
stub_fiscal_tax_residence = {
    "fiscal_tax_residence": dummy_fiscal_tax_residence,
    "_id": None,
}


@patch.object(Gladsheim, "error")
async def test_update_user_and_broker_member_raising_not_finding_user(
    mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.side_effect = None
    fake_infra.get_client.return_value[
        dummy_env
    ].__getitem__.return_value = fake_collection
    fake_collection.update_one.return_value.matched_count = None
    with pytest.raises(UserWasNotFound) as error:
        await UserRepository.update_user_and_broker_member(
            dummy_unique_id, dummy_is_exchange_member
        )
        assert str(error) == dummy_unique_id
    fake_collection.update_one.assert_called_with(
        dummy_user_filter, dummy_update_fields
    )


@patch.object(Gladsheim, "error")
async def test_update_user_and_broker_member(mocked_logger, monkeypatch):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[
        dummy_env
    ].__getitem__.return_value = fake_collection
    fake_collection.update_one.return_value.matched_count = 1
    result = await UserRepository.update_user_and_broker_member(
        dummy_unique_id, dummy_is_exchange_member
    )
    fake_collection.update_one.assert_called_with(
        dummy_user_filter, dummy_update_fields
    )
    assert result is True
    mocked_logger.assert_not_called()


@patch.object(Gladsheim, "error")
async def test_update_user_and_broker_member_raising_commum_error(
    mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    internal_error = ValueError()
    fake_infra.get_client.return_value[
        dummy_env
    ].__getitem__.return_value = fake_collection
    fake_collection.update_one.side_effect = internal_error
    result = await UserRepository.update_user_and_broker_member(
        dummy_unique_id, dummy_is_exchange_member
    )
    assert result is False
    fake_collection.update_one.assert_called_with(
        dummy_user_filter, dummy_update_fields
    )
    mocked_logger.assert_called_once_with(
        error=internal_error,
        message="UserRepository::update_user::Failed to update user",
        query=dummy_user_filter,
    )
