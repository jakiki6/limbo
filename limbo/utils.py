def unpack_varint(buf):
    nread = 0
    res = 0
    while True:
        read = buf.read(1)[0]
        val = (read & 0b01111111)
        res |= (val << (7 * nread))
        nread += 1
        if nread > 5:
            raise Exception("VarInt too long")
        if (read & 0b10000000) == 0:
            break
    return res

def pack_varint(val):
    res = b""
    while True:
        temp = val & 0b11111111
        val >>= 7;
        if val != 0:
            temp |= 0b10000000
        res += bytes([temp])
        if val == 0:
            break
    return res
