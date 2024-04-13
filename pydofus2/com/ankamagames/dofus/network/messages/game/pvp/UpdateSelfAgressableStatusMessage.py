from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class UpdateSelfAgressableStatusMessage(NetworkMessage):
    status: int
    probationTime: int
    roleAvAId: int
    pictoScore: int

    def init(self, status_: int, probationTime_: int, roleAvAId_: int, pictoScore_: int):
        self.status = status_
        self.probationTime = probationTime_
        self.roleAvAId = roleAvAId_
        self.pictoScore = pictoScore_

        super().__init__()
