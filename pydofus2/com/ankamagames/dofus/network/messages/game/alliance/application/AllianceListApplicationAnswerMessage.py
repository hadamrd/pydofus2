from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.PaginationAnswerAbstractMessage import \
    PaginationAnswerAbstractMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.application.SocialApplicationInformation import \
        SocialApplicationInformation


class AllianceListApplicationAnswerMessage(PaginationAnswerAbstractMessage):
    applies: list["SocialApplicationInformation"]

    def init(self, applies_: list["SocialApplicationInformation"], offset_: int, count_: int, total_: int):
        self.applies = applies_

        super().init(offset_, count_, total_)
