from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.achievement.Achievement import \
        Achievement
    

class AchievementDetailsMessage(NetworkMessage):
    achievement: 'Achievement'
    def init(self, achievement_: 'Achievement'):
        self.achievement = achievement_
        
        super().__init__()
    