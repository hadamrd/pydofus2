from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.fight.arena.GameRolePlayArenaUpdatePlayerInfosMessage import \
    GameRolePlayArenaUpdatePlayerInfosMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.fight.arena.ArenaRankInfos import \
        ArenaRankInfos
    

class GameRolePlayArenaUpdatePlayerInfosAllQueuesMessage(GameRolePlayArenaUpdatePlayerInfosMessage):
    team: 'ArenaRankInfos'
    duel: 'ArenaRankInfos'
    def init(self, team_: 'ArenaRankInfos', duel_: 'ArenaRankInfos', solo_: 'ArenaRankInfos'):
        self.team = team_
        self.duel = duel_
        
        super().init(solo_)
    