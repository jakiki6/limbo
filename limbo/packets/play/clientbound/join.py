from ...packet import Packet
from ....types import Int, Long, Boolean, UnsignedByte, Byte, Array, Identifier, NbtTagCompound, VarInt

class JoinGamePacket(Packet):
    structure = {
        "entity_id": Int(),
        "is_hardcore": Boolean(),
        "gamemode": UnsignedByte(),
        "previous_gamemode": Byte(),
        "world_count": VarInt(),
        "world_names": Array(Identifier()),
        "dimension_codec": NbtTagCompound(),
        "dimension": NbtTagCompound(),
        "world_name": Identifier(),
        "hashed_seed": Long(),
        "max_players": VarInt(),
        "view_distance": VarInt(),
        "reduced_debug_info": Boolean(),
        "enable_respawn_screen": Boolean(),
        "is_debug": Boolean(),
        "is_flat": Boolean()
    }

    id = 0x26
