from ...packet import Packet
from ....types import VarInt, String, UnsignedShort

class HandShakePacket(Packet):
    structure = {
        "protocol_version": VarInt(),
        "server_address": String(length=255),
        "server_port": UnsignedShort(),
        "next_state": VarInt()
    }

    id = 0x00
