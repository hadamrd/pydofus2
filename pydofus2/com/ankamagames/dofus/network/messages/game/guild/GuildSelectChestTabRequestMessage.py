from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GuildSelectChestTabRequestMessage(NetworkMessage):
    tabNumber: int

    def init(self, tabNumber_: int):
        self.tabNumber = tabNumber_

        super().__init__()
