from pydofus2.com.ankamagames.dofus.network.messages.game.PaginationAnswerAbstractMessage import PaginationAnswerAbstractMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformations import AllianceFactSheetInformations
    

class AllianceSummaryMessage(PaginationAnswerAbstractMessage):
    alliances: list['AllianceFactSheetInformations']
    def init(self, alliances_: list['AllianceFactSheetInformations'], offset_: int, count_: int, total_: int):
        self.alliances = alliances_
        
        super().init(offset_, count_, total_)
    