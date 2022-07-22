# STANDARD IMPORTS
from pydantic import BaseModel


class ExchangeMemberRequest(BaseModel):
    exchange_member: bool


class ExchangeMemberTemplates:

    @classmethod
    def exchange_member_schema_template(
            cls, exchange_member: bool, unique_id: str
    ) -> dict:
        broker_member_template = {
            "unique_id": unique_id,
            "exchange_member": exchange_member
        }

        return broker_member_template
