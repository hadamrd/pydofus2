from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class AllianceChangeMemberRankMessage(NetworkMessage):
    memberId: int
    rankId: int

    def init(self, memberId_: int, rankId_: int):
        self.memberId = memberId_
        self.rankId = rankId_

        super().__init__()
