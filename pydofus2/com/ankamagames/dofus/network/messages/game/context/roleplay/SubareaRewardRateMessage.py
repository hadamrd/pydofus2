from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class SubareaRewardRateMessage(NetworkMessage):
    subAreaRate: int

    def init(self, subAreaRate_: int):
        self.subAreaRate = subAreaRate_

        super().__init__()
