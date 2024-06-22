from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class SwitchArenaXpRewardsModeMessage(NetworkMessage):
    xpRewards: bool

    def init(self, xpRewards_: bool):
        self.xpRewards = xpRewards_

        super().__init__()
