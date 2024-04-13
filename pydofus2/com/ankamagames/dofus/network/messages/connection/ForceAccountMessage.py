from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ForceAccountMessage(NetworkMessage):
    accountId: int

    def init(self, accountId_: int):
        self.accountId = accountId_

        super().__init__()
