from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class InteractiveUseErrorMessage(NetworkMessage):
    elemId: int
    skillInstanceUid: int

    def init(self, elemId_: int, skillInstanceUid_: int):
        self.elemId = elemId_
        self.skillInstanceUid = skillInstanceUid_

        super().__init__()
