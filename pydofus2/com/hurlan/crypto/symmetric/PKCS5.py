from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.hurlan.crypto.symmetric.IPad import IPad


class PKCS5(IPad):

    blockSize: int

    def __init__(self, blockSize: int = 0):
        super().__init__()
        self.blockSize = blockSize

    def pad(self, a: ByteArray):
        c: int = self.blockSize - (a.length % self.blockSize)
        for _ in range(c):
            a.writeByte(c)

    def unpad(self, a: ByteArray) -> None:
        if a.length % self.blockSize != 0:
            raise Exception("PKCS#5::unpad: ByteArray.length isn't a multiple of the blockSize")
        c = a[-1]
        for _ in range(c):
            Logger().debug("PKCS#5::unpad: %s", a[-1])
            v = a[-1]
            del a[-1]
            if c != v:
                raise Exception(f"PKCS#5:unpad: Invalid padding value. expected [{c}], found [{v}]")

    def setBlockSize(self, bs: int) -> None:
        self.blockSize = bs
