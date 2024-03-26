from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.fight.arena.ArenaRankInfos import \
        ArenaRankInfos


class GameRolePlayArenaUpdatePlayerInfosMessage(NetworkMessage):
    arenaRanks: list["ArenaRankInfos"]
    banEndDate: int

    def init(self, arenaRanks_: list["ArenaRankInfos"], banEndDate_: int):
        self.arenaRanks = arenaRanks_
        self.banEndDate = banEndDate_

        super().__init__()
