from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.alliance.AllianceMemberInfo import AllianceMemberInfo
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorInformations import (
        TaxCollectorInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismGeolocalizedInformation import (
        PrismGeolocalizedInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.social.AllianceFactSheetInformation import (
        AllianceFactSheetInformation,
    )


class AllianceInsiderInfoMessage(NetworkMessage):
    allianceInfos: "AllianceFactSheetInformation"
    members: list["AllianceMemberInfo"]
    prisms: list["PrismGeolocalizedInformation"]
    taxCollectors: list["TaxCollectorInformations"]

    def init(
        self,
        allianceInfos_: "AllianceFactSheetInformation",
        members_: list["AllianceMemberInfo"],
        prisms_: list["PrismGeolocalizedInformation"],
        taxCollectors_: list["TaxCollectorInformations"],
    ):
        self.allianceInfos = allianceInfos_
        self.members = members_
        self.prisms = prisms_
        self.taxCollectors = taxCollectors_

        super().__init__()
