from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class GuildInformationsGeneralMessage(NetworkMessage):
    abandonnedPaddock: bool
    level: int
    expLevelFloor: int
    experience: int
    expNextLevelFloor: int
    creationDate: int

    def init(
        self,
        abandonnedPaddock_: bool,
        level_: int,
        expLevelFloor_: int,
        experience_: int,
        expNextLevelFloor_: int,
        creationDate_: int,
    ):
        self.abandonnedPaddock = abandonnedPaddock_
        self.level = level_
        self.expLevelFloor = expLevelFloor_
        self.experience = experience_
        self.expNextLevelFloor = expNextLevelFloor_
        self.creationDate = creationDate_

        super().__init__()
