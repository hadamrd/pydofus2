from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.TaxCollectorStaticInformations import (
    TaxCollectorStaticInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformations import (
        AllianceInformations,
    )


class TaxCollectorStaticExtendedInformations(TaxCollectorStaticInformations):
    allianceIdentity: "AllianceInformations"

    def init(self, firstNameId_: int, lastNameId_: int, allianceIdentity_: "AllianceInformation", callerId_: int):
        self.allianceIdentity = allianceIdentity_

        super().init(firstNameId_, lastNameId_, allianceIdentity_, callerId_)
