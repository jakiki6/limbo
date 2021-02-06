from ...packet import Packet
from ....types import String

class LoginStartPacket(Packet):
    structure = {
        "name": String(16)
    }

    id = 0x00
