from ...packet import Packet
from ....types import Long

class PingPacket(Packet):
    structure = {
        "payload": Long()
    }

    id = 0x01
