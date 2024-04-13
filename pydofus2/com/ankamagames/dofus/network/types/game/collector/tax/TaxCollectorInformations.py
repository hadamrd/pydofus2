from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristics import (
        CharacterCharacteristics,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.AdditionalTaxCollectorInformation import (
        AdditionalTaxCollectorInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorComplementaryInformations import (
        TaxCollectorComplementaryInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import (
        TaxCollectorOrderedSpell,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import ObjectItem
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class TaxCollectorInformations(NetworkMessage):
    uniqueId: int
    firstNameId: int
    lastNameId: int
    allianceIdentity: "AllianceInformation"
    additionalInfos: "AdditionalTaxCollectorInformation"
    worldX: int
    worldY: int
    subAreaId: int
    state: int
    look: "EntityLook"
    complements: list["TaxCollectorComplementaryInformations"]
    characteristics: "CharacterCharacteristics"
    equipments: list["ObjectItem"]
    spells: list["TaxCollectorOrderedSpell"]

    def init(
        self,
        uniqueId_: int,
        firstNameId_: int,
        lastNameId_: int,
        allianceIdentity_: "AllianceInformation",
        additionalInfos_: "AdditionalTaxCollectorInformation",
        worldX_: int,
        worldY_: int,
        subAreaId_: int,
        state_: int,
        look_: "EntityLook",
        complements_: list["TaxCollectorComplementaryInformations"],
        characteristics_: "CharacterCharacteristics",
        equipments_: list["ObjectItem"],
        spells_: list["TaxCollectorOrderedSpell"],
    ):
        self.uniqueId = uniqueId_
        self.firstNameId = firstNameId_
        self.lastNameId = lastNameId_
        self.allianceIdentity = allianceIdentity_
        self.additionalInfos = additionalInfos_
        self.worldX = worldX_
        self.worldY = worldY_
        self.subAreaId = subAreaId_
        self.state = state_
        self.look = look_
        self.complements = complements_
        self.characteristics = characteristics_
        self.equipments = equipments_
        self.spells = spells_

        super().__init__()
