from ...packet import Packet
from ....types import String, UUID

class LoginDisconnectPacket(Packet):
    structure = {
        "reason": String(32767)
    }

    id = 0x00

class LoginSuccessPacket(Packet):
    structure = {
        "uuid": UUID(),
        "username": String(16)
    }

    id = 0x02
