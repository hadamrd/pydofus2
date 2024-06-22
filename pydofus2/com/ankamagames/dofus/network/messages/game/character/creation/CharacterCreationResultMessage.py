from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class CharacterCreationResultMessage(NetworkMessage):
    result: int
    reason: int

    def init(self, result_: int, reason_: int):
        self.result = result_
        self.reason = reason_

        super().__init__()
