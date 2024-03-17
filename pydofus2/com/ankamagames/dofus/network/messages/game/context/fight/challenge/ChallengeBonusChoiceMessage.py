from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ChallengeBonusChoiceMessage(NetworkMessage):
    challengeBonus: int
    def init(self, challengeBonus_: int):
        self.challengeBonus = challengeBonus_
        
        super().__init__()
    