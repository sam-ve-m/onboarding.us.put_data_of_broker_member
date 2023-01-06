from pydantic import BaseModel

from func.src.domain.models.device_info.model import DeviceInfo


class ExchangeMemberRequest(BaseModel):
    exchange_member: bool


class ExchangeMemberToPersephone:
    @classmethod
    def exchange_member_schema(
        cls, exchange_member: bool, unique_id: str, device_info: DeviceInfo
    ) -> dict:
        broker_member_template = {
            "unique_id": unique_id,
            "exchange_member": exchange_member,
            "device_info": device_info.device_info,
            "device_id": device_info.device_id,
        }

        return broker_member_template
