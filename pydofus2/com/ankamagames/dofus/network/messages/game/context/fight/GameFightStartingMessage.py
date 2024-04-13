from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameFightStartingMessage(NetworkMessage):
    fightType: int
    fightId: int
    attackerId: int
    defenderId: int
    containsBoss: bool
    monsters: list[int]

    def init(
        self,
        fightType_: int,
        fightId_: int,
        attackerId_: int,
        defenderId_: int,
        containsBoss_: bool,
        monsters_: list[int],
    ):
        self.fightType = fightType_
        self.fightId = fightId_
        self.attackerId = attackerId_
        self.defenderId = defenderId_
        self.containsBoss = containsBoss_
        self.monsters = monsters_

        super().__init__()
