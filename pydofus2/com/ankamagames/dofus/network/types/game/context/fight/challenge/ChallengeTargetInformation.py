from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ChallengeTargetInformation(NetworkMessage):
    targetId: int
    targetCell: int

    def init(self, targetId_: int, targetCell_: int):
        self.targetId = targetId_
        self.targetCell = targetCell_

        super().__init__()
