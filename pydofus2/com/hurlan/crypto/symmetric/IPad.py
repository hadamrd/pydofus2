from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray


class IPad:
    def pad(self, src: ByteArray) -> None:
        raise NotImplementedError()

    def unpad(self, src: ByteArray) -> None:
        raise NotImplementedError()

    def setBlockSize(self, blockSize: int) -> None:
        raise NotImplementedError()
