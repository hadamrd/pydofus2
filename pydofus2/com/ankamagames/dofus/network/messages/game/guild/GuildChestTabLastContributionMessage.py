from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GuildChestTabLastContributionMessage(NetworkMessage):
    lastContributionDate: int

    def init(self, lastContributionDate_: int):
        self.lastContributionDate = lastContributionDate_

        super().__init__()
