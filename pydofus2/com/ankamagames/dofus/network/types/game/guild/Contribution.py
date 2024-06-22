from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class Contribution(NetworkMessage):
    contributorId: int
    contributorName: str
    amount: int

    def init(self, contributorId_: int, contributorName_: str, amount_: int):
        self.contributorId = contributorId_
        self.contributorName = contributorName_
        self.amount = amount_

        super().__init__()
