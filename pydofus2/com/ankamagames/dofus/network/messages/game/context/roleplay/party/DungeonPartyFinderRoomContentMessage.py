from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.party.DungeonPartyFinderPlayer import \
        DungeonPartyFinderPlayer


class DungeonPartyFinderRoomContentMessage(NetworkMessage):
    dungeonId: int
    players: list["DungeonPartyFinderPlayer"]

    def init(self, dungeonId_: int, players_: list["DungeonPartyFinderPlayer"]):
        self.dungeonId = dungeonId_
        self.players = players_

        super().__init__()
