from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.PaginationAnswerAbstractMessage import \
    PaginationAnswerAbstractMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformation import \
        AllianceFactSheetInformation
    

class AllianceSummaryMessage(PaginationAnswerAbstractMessage):
    alliances: list['AllianceFactSheetInformation']
    def init(self, alliances_: list['AllianceFactSheetInformation'], offset_: int, count_: int, total_: int):
        self.alliances = alliances_
        
        super().init(offset_, count_, total_)
    