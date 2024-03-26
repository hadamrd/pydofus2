from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import \
    BasicNamedAllianceInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.GuildEmblem import \
        GuildEmblem


class AllianceInformations(BasicNamedAllianceInformations):
    allianceEmblem: "GuildEmblem"

    def init(self, allianceEmblem_: "GuildEmblem", allianceName_: str, allianceId_: int, allianceTag_: str):
        self.allianceEmblem = allianceEmblem_

        super().init(allianceName_, allianceId_, allianceTag_)
