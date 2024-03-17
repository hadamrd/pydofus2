from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.DungeonPartyFinderPlayer import \
        DungeonPartyFinderPlayer
    

class DungeonPartyFinderRoomContentUpdateMessage(NetworkMessage):
    dungeonId: int
    addedPlayers: list['DungeonPartyFinderPlayer']
    removedPlayersIds: list[int]
    def init(self, dungeonId_: int, addedPlayers_: list['DungeonPartyFinderPlayer'], removedPlayersIds_: list[int]):
        self.dungeonId = dungeonId_
        self.addedPlayers = addedPlayers_
        self.removedPlayersIds = removedPlayersIds_
        
        super().__init__()
    