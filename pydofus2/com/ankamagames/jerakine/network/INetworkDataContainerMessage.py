from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray


class INetworkDataContainerMessage:
    @property
    def content() -> ByteArray:
        raise NotImplementedError("This method must be overriden")

    @content.setter
    def content(self, value: ByteArray):
        raise NotImplementedError("This method must be overriden")
