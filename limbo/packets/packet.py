import io

class Packet(object):
    structure = {}
    id = 0x00

    def __init__(self):
        for key, val in self.__class__.structure.items():
            setattr(self, key, None)
    @classmethod
    def unpack(cls, buf):
        packet = cls()
        for key, val in cls.structure.items():
            setattr(packet, key, val.read(buf))
        return packet
    def pack(self):
        buf = io.BytesIO(b"")
        for key, val in self.__class__.structure.items():
            getattr(self, key).write(buf)
        return buf.getvalue()
    def __repr__(self):
        res = ""
        for key, val in self.__class__.structure.items():
            res += f"{key}={getattr(self, key).val}, "
        return f"{self.__class__.__name__}({res[:-2]})"
