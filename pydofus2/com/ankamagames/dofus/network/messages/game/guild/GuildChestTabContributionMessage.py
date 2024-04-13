from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GuildChestTabContributionMessage(NetworkMessage):
    tabNumber: int
    requiredAmount: int
    currentAmount: int
    chestContributionEnrollmentDelay: int
    chestContributionDelay: int

    def init(
        self,
        tabNumber_: int,
        requiredAmount_: int,
        currentAmount_: int,
        chestContributionEnrollmentDelay_: int,
        chestContributionDelay_: int,
    ):
        self.tabNumber = tabNumber_
        self.requiredAmount = requiredAmount_
        self.currentAmount = currentAmount_
        self.chestContributionEnrollmentDelay = chestContributionEnrollmentDelay_
        self.chestContributionDelay = chestContributionDelay_

        super().__init__()
