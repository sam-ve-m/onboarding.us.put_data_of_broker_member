# STANDARD IMPORTS
from decouple import config

# PROJECT IMPORTS
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    def update_user_and_exchange_member(cls, unique_id: str, exchange_member: bool):
        try:
            user_exchange_member_was_updated = await cls.update_one(
                old={"unique_id": unique_id},
                new={"external_exchange_requirements.us.is_exchange_member": exchange_member},
            )
            return user_exchange_member_was_updated
        except Exception as error:
            Gladsheim.error(error=error)
            return False
