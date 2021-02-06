from ...packet import Packet
from ....types import String

class LoginDisconnectPacket(Packet):
    structure = {
        "reason": String(32767)
    }

    id = 0x00
