from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GroupTeleportPlayerAnswerMessage(NetworkMessage):
    accept: bool
    requesterId: int

    def init(self, accept_: bool, requesterId_: int):
        self.accept = accept_
        self.requesterId = requesterId_

        super().__init__()
