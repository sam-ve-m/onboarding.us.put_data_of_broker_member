# STANDARD IMPORTS
from decouple import config

# PROJECT IMPORTS
from src.domain.models.jwt.response import Jwt
from src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

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
    async def update_user_and_broker_member(cls, jwt_data: Jwt):
        try:
            collection = await cls.__get_collection()

            user_exchange_member_was_updated = await collection.update_one(
                old={"unique_id":
                    jwt_data.get_unique_id_from_jwt_payload()},
                new={"external_exchange_requirements.us.is_exchange_member":
                    jwt_data.get_exchange_member_from_jwt_payload()},
            )
            return user_exchange_member_was_updated

        except Exception as error:
            Gladsheim.error(error=error)
            return False
