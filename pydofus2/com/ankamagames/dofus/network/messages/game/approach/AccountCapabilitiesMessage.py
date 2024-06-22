from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AccountCapabilitiesMessage(NetworkMessage):
    accountId: int
    status: int
    tutorialAvailable: bool
    canCreateNewCharacter: bool
    tutorialAvailable: bool
    canCreateNewCharacter: bool

    def init(self, accountId_: int, status_: int, tutorialAvailable_: bool, canCreateNewCharacter_: bool):
        self.accountId = accountId_
        self.status = status_
        self.tutorialAvailable = tutorialAvailable_
        self.canCreateNewCharacter = canCreateNewCharacter_

        super().__init__()
