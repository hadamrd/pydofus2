from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.alignment.ActorExtendedAlignmentInformations import (
        ActorExtendedAlignmentInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristic import (
        CharacterCharacteristic,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.character.spellmodifier.SpellModifierMessage import (
        SpellModifierMessage,
    )


class CharacterCharacteristicsInformations(NetworkMessage):
    experience: int
    experienceLevelFloor: int
    experienceNextLevelFloor: int
    experienceBonusLimit: int
    kamas: int
    alignmentInfos: "ActorExtendedAlignmentInformations"
    criticalHitWeapon: int
    characteristics: list["CharacterCharacteristic"]
    spellModifiers: list["SpellModifierMessage"]
    probationTime: int

    def init(
        self,
        experience_: int,
        experienceLevelFloor_: int,
        experienceNextLevelFloor_: int,
        experienceBonusLimit_: int,
        kamas_: int,
        alignmentInfos_: "ActorExtendedAlignmentInformations",
        criticalHitWeapon_: int,
        characteristics_: list["CharacterCharacteristic"],
        spellModifiers_: list["SpellModifierMessage"],
        probationTime_: int,
    ):
        self.experience = experience_
        self.experienceLevelFloor = experienceLevelFloor_
        self.experienceNextLevelFloor = experienceNextLevelFloor_
        self.experienceBonusLimit = experienceBonusLimit_
        self.kamas = kamas_
        self.alignmentInfos = alignmentInfos_
        self.criticalHitWeapon = criticalHitWeapon_
        self.characteristics = characteristics_
        self.spellModifiers = spellModifiers_
        self.probationTime = probationTime_

        super().__init__()
