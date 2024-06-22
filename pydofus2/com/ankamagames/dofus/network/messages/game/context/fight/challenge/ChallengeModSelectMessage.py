from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ChallengeModSelectMessage(NetworkMessage):
    challengeMod: int

    def init(self, challengeMod_: int):
        self.challengeMod = challengeMod_

        super().__init__()
