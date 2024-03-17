from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.GameRolePlayNpcQuestFlag import \
        GameRolePlayNpcQuestFlag
    

class MapNpcQuestInfo(NetworkMessage):
    mapId: int
    npcsIdsWithQuest: list[int]
    questFlags: list['GameRolePlayNpcQuestFlag']
    def init(self, mapId_: int, npcsIdsWithQuest_: list[int], questFlags_: list['GameRolePlayNpcQuestFlag']):
        self.mapId = mapId_
        self.npcsIdsWithQuest = npcsIdsWithQuest_
        self.questFlags = questFlags_
        
        super().__init__()
    