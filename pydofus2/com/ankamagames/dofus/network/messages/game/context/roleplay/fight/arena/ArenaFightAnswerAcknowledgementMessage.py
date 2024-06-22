from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ArenaFightAnswerAcknowledgementMessage(NetworkMessage):
    acknowledged: bool

    def init(self, acknowledged_: bool):
        self.acknowledged = acknowledged_

        super().__init__()
