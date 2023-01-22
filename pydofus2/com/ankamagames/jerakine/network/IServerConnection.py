from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.messages.MessageHandler import MessageHandler
from pydofus2.com.ankamagames.jerakine.network.ILagometer import ILagometer
from pydofus2.com.ankamagames.jerakine.network.RawDataParser import RawDataParser


class IServerConnection:
    
    @property
    def rawParser(self) -> RawDataParser:
        raise NotImplementedError()

    @rawParser.setter
    def rawParser(self, param1: RawDataParser) -> None:
        raise NotImplementedError()

    @property
    def handler(self) -> MessageHandler:
        raise NotImplementedError()

    @handler.setter
    def handler(self, param1: MessageHandler) -> None:
        raise NotImplementedError()

    def pauseBuffer(self) -> list:
        raise NotImplementedError()

    @property
    def connected(self) -> bool:
        raise NotImplementedError()

    @property
    def connecting(self) -> bool:
        raise NotImplementedError()

    def latencyAvg(self) -> int:
        raise NotImplementedError()

    def latencySamplesCount(self) -> int:
        raise NotImplementedError()

    def latencySamplesMax(self) -> int:
        raise NotImplementedError()

    @property
    def lagometer(self) -> ILagometer:
        raise NotImplementedError()

    @lagometer.setter
    def lagometer(self, param1: ILagometer) -> None:
        raise NotImplementedError()

    def connect(self, param1: str, param2: int) -> None:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()

    def pause(self) -> None:
        raise NotImplementedError()

    def resume(self) -> None:
        raise NotImplementedError()

    def send(self, param1: INetworkMessage, param2: str = "") -> None:
        raise NotImplementedError()

    def stopConnectionTimeout(self) -> None:
        raise NotImplementedError()

    def checkClosed(self) -> None:
        raise NotImplementedError()