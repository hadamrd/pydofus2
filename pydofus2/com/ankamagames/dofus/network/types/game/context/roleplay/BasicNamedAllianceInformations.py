from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import (
    BasicAllianceInformations,
)


class BasicNamedAllianceInformations(BasicAllianceInformations):
    allianceName: str

    def init(self, allianceName_: str, allianceId_: int, allianceTag_: str):
        self.allianceName = allianceName_

        super().init(allianceId_, allianceTag_)
