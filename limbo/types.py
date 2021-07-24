import struct, uuid, pynbt
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

class Int(Type):
    def __init__(self, val=0):
        self.val = val
    def read(self, buf):
        val = struct.unpack('>i', buf.read(4))[0]
        return self.__class__(val)
    def write(self, buf): 
        buf.write(struct.pack('>i', self.val))

class Boolean(Type):
    def __init__(self, val=False):
        self.val = val
    def read(self, buf): 
        val = struct.unpack('?', buf.read(1))[0]
        return self.__class__(val)
    def write(self, buf):
        buf.write(struct.pack('?', self.val))

class Byte(Type):
    def __init__(self, val=0x00):
        self.val = val
    def read(self, buf):
        val = struct.unpack('b', buf.read(1))[0]
        return self.__class__(val)
    def write(self, buf):
        buf.write(struct.pack('b', self.val))

class UnsignedByte(Type):
    def __init__(self, val=0x00):
        self.val = val
    def read(self, buf):
        val = struct.unpack('B', buf.read(1))[0]
        return self.__class__(val)
    def write(self, buf):
        buf.write(struct.pack('B', self.val))

class Array(Type):
    def __init__(self, val=[], num=-1, type=None):
        self.val = val
        self.num = num
        self.type = type
    def read(self, buf):
        assert self.type != None, "Type not set"
        assert self.num != -1, "Invalid number of items"

        vals = []
        for i in range(0, self.num):
            vals.append(self.type.read(buf))

        return vals
    def write(self, buf):
        for val in self.val:
            val.write(buf)

class Identifier(String): pass

class NbtTagCompound(Type):
    def __init__(self, val={}):
        self.val = val
    def read(self, buf):
        val = pynbt.NBTFile(self.val)
        return self.__class__(dict(val))
    def write(self, buf):
        pynbt.NBTFile(value=self.val).save(buf)
