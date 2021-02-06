from ...packet import Packet
from ....types import Long

class PongPacket(Packet):
    structure = {
        "payload": Long()
    }

    id = 0x01
