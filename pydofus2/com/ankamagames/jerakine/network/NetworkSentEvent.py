from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class NetworkSentEvent:

    EVENT_SENT = "messageSent"

    _message: INetworkMessage

    def __init__(self, msg: INetworkMessage):
        super().__init__()
        self._message = msg

    @property
    def message(self) -> INetworkMessage:
        return self._message
