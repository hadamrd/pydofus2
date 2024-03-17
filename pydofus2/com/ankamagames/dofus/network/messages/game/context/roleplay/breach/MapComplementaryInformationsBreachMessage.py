from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import \
    MapComplementaryInformationsDataMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightCommonInformations import \
        FightCommonInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightStartingPositions import \
        FightStartingPositions
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.breach.BreachBranch import \
        BreachBranch
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
        GameRolePlayActorInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformations import \
        HouseInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import \
        InteractiveElement
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.MapObstacle import \
        MapObstacle
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.StatedElement import \
        StatedElement
    

class MapComplementaryInformationsBreachMessage(MapComplementaryInformationsDataMessage):
    floor: int
    room: int
    infinityMode: int
    branches: list['BreachBranch']
    def init(self, floor_: int, room_: int, infinityMode_: int, branches_: list['BreachBranch'], subAreaId_: int, mapId_: int, houses_: list['HouseInformations'], actors_: list['GameRolePlayActorInformations'], interactiveElements_: list['InteractiveElement'], statedElements_: list['StatedElement'], obstacles_: list['MapObstacle'], fights_: list['FightCommonInformations'], hasAggressiveMonsters_: bool, fightStartPositions_: 'FightStartingPositions'):
        self.floor = floor_
        self.room = room_
        self.infinityMode = infinityMode_
        self.branches = branches_
        
        super().init(subAreaId_, mapId_, houses_, actors_, interactiveElements_, statedElements_, obstacles_, fights_, hasAggressiveMonsters_, fightStartPositions_)
    