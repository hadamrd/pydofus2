from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.application.ApplicationPlayerInformation import \
        ApplicationPlayerInformation


class SocialApplicationInformation(NetworkMessage):
    playerInfo: "ApplicationPlayerInformation"
    applyText: str
    creationDate: int

    def init(self, playerInfo_: "ApplicationPlayerInformation", applyText_: str, creationDate_: int):
        self.playerInfo = playerInfo_
        self.applyText = applyText_
        self.creationDate = creationDate_

        super().__init__()
