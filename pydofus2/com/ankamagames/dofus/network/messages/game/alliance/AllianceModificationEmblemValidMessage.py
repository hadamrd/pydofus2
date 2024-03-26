from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class AllianceModificationEmblemValidMessage(NetworkMessage):
    allianceEmblem: "SocialEmblem"

    def init(self, allianceEmblem_: "SocialEmblem"):
        self.allianceEmblem = allianceEmblem_

        super().__init__()
