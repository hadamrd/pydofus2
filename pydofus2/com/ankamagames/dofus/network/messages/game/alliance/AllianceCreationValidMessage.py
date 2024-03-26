from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.social.SocialEmblem import \
        SocialEmblem


class AllianceCreationValidMessage(NetworkMessage):
    allianceName: str
    allianceTag: str
    allianceEmblem: "SocialEmblem"

    def init(self, allianceName_: str, allianceTag_: str, allianceEmblem_: "SocialEmblem"):
        self.allianceName = allianceName_
        self.allianceTag = allianceTag_
        self.allianceEmblem = allianceEmblem_

        super().__init__()
