from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class ILagometer:
    def ping(self, param1: INetworkMessage = None) -> None:
        raise NotImplementedError("This method must be overriden")

    def pong(self, param1: INetworkMessage = None) -> None:
        raise NotImplementedError("This method must be overriden")

    def stop(self) -> None:
        raise NotImplementedError("This method must be overriden")
