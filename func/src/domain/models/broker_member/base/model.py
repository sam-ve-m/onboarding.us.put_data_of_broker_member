# STANDARD IMPORTS
from pydantic import BaseModel


class ExchangeMemberRequest(BaseModel):
    exchange_member: bool


class ExchangeMemberToPersephone:
    @classmethod
    def exchange_member_schema(cls, exchange_member: bool, unique_id: str) -> dict:
        broker_member_template = {
            "unique_id": unique_id,
            "exchange_member": exchange_member,
        }

        return broker_member_template
