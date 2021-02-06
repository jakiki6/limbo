from ...packet import Packet
from ....types import String

class ResponsePacket(Packet):
    structure = {
        "json_response": String(length=32767)
    }

    id = 0x00
