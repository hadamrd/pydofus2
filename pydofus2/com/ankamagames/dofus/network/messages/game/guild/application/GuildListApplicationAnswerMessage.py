from pydofus2.com.ankamagames.dofus.network.messages.game.PaginationAnswerAbstractMessage import PaginationAnswerAbstractMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.application.GuildApplicationInformation import GuildApplicationInformation
    

class GuildListApplicationAnswerMessage(PaginationAnswerAbstractMessage):
    applies: list['GuildApplicationInformation']
    def init(self, applies_: list['GuildApplicationInformation'], offset_: int, count_: int, total_: int):
        self.applies = applies_
        
        super().init(offset_, count_, total_)
    