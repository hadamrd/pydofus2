from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ChallengeNumberMessage(NetworkMessage):
    challengeNumber: int

    def init(self, challengeNumber_: int):
        self.challengeNumber = challengeNumber_

        super().__init__()
