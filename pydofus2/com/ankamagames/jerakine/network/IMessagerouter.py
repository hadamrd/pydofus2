from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class IMessageRouter:
    def getConnectionId(param1: INetworkMessage) -> str:
        raise NotImplementedError("This method must be overriden")
