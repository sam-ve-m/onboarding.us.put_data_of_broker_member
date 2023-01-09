# STANDARD IMPORTS
from decouple import config

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import UserWasNotFound
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::__get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=cls.database,
                collection=cls.collection,
            )
            raise ex

    @classmethod
    async def update_user_and_broker_member(
        cls, unique_id: str, exchange_member_request: bool
    ):
        user_filter = {"unique_id": unique_id}
        exchange_member = {
            "$set": {
                "external_exchange_requirements.us.is_exchange_member": exchange_member_request
            }
        }

        collection = await cls.__get_collection()
        try:
            was_updated = await collection.update_one(user_filter, exchange_member)
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message="UserRepository::update_user::Failed to update user",
                query=user_filter,
            )
            return False

        if not was_updated.matched_count == 1:
            raise UserWasNotFound
        return bool(was_updated)
