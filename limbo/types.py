import struct, uuid
from . import utils

class Type(object):
    def __init__(self, val=None):
        self.val = val
    def read(self, buf):
        return self.__class__()
    def write(self, buf):
        pass

class VarInt(Type):
    def __init__(self, val=0):
        self.val = val
    def read(self, buf):
        val = utils.unpack_varint(buf)
        return self.__class__(val)
    def write(self, buf):
         buf.write(utils.pack_varint(self.val))

class String(Type):
    def __init__(self, val="", length=255):
        self.val = val
        self.length = length
    def read(self, buf):
        length = utils.unpack_varint(buf)
        val = buf.read(length).decode("utf-8")
        return self.__class__(val, self.length)
    def write(self, buf):
        val = self.val.encode("utf-8")
        if not len(val) <= self.length * 4:
            raise Exception(f"{len(val)} is too big (should be at most {self.length})")
        buf.write(utils.pack_varint(len(self.val)))
        buf.write(val)

class UnsignedShort(Type):
    def __init__(self, val=0):
        self.val = val
    def read(self, buf):
        val = struct.unpack('>H', buf.read(2))[0]
        return self.__class__(val)
    def write(self, buf):
        buf.write(struct.pack('>h', self.val))

class RawBytes(Type):
    def __init__(self, val=b""):
        self.val = val
    def read(self, buf):
        return self.__class__(buf.read())
    def write(self, buf):
        buf.write(self.val)

class Nop(Type):
    pass

class Long(Type):
    def __init__(self, val=0):
        self.val = val
    def read(self, buf):
        val = struct.unpack('>q', buf.read(8))[0]
        return self.__class__(val)
    def write(self, buf):
        buf.write(struct.pack('>q', self.val))

class UUID(Type):
    def __init__(self, val=uuid.UUID(bytes=bytes(16))):
        self.val = val
    def read(self, buf):
        return self.__class__(uuid.UUID(bytes=buf.read(16)))
    def write(self, buf):
        buf.write(self.val.bytes)
