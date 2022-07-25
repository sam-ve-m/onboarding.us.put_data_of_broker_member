# STANDARD IMPORTS
# from decouple import config
from src.infrastructure.env_config import config

# PROJECT IMPORTS
from src.domain.models.jwt.response import Jwt
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def update_user_and_exchange_member(cls, jwt_data: Jwt):
        try:
            user_exchange_member_was_updated = await cls.update_one(
                old={"unique_id":
                    jwt_data.get_unique_id_from_jwt_payload()},
                new={"external_exchange_requirements.us.is_exchange_member":
                    jwt_data.get_exchange_member_from_jwt_payload()},
            )
            return user_exchange_member_was_updated
        except Exception as error:
            Gladsheim.error(error=error)
            return False
