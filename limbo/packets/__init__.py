import io, json
from mergedeep import merge

from .. import utils

mapping = {}

from .handshake import mapping as hmapping
from .status import mapping as smapping
from .login import mapping as lmapping
merge(mapping, hmapping, smapping, lmapping)

print(f"Dump of registered packets:")
for key, val in mapping.items():
    print(f"state {key}:")
    for key2, val2 in val.items():
        print(f"    0x{hex(key2)[2:].zfill(2)}: {val2}")

def unpack(buf, state):
    packet_id, buf = unpack_packet(buf, state)
    try:
        return mapping[state][packet_id].unpack(buf)
    except:
        print(f"unknown packet {packet_id} in state {state}")

def pack(packet):
    buf = io.BytesIO()
    val = packet.pack()
    id = utils.pack_varint(packet.id)
    length = utils.pack_varint(len(id) + len(val))

    buf.write(length)
    buf.write(id)
    buf.write(val)

    return buf.getvalue()

def unpack_packet(buf, state):
    buf = io.BytesIO(buf)
    length = utils.unpack_varint(buf)

    packet_id = utils.unpack_varint(buf)

    return packet_id, buf

def send(packet, socket):
    buf = pack(packet)
    print(f"-> {packet} ({len(buf)})")
    socket.send(buf)
