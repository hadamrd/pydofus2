from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import \
    SpellWrapper

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame import (
        PlayedCharacterUpdatesFrame,
    )

from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
    CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicDetailed import \
    CharacterCharacteristicDetailed
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import \
    CharacterCharacteristicsInformations
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable


class FightFighterStatsListStep(AbstractSequencable, IFightStep):

    _playerId: float

    _stats: CharacterCharacteristicsInformations

    def __init__(self, stats: CharacterCharacteristicsInformations):
        super().__init__()
        self._stats = stats

    @property
    def stepType(self) -> str:
        return "fighterStatsList"

    def start(self) -> None:
        self._playerId = CurrentPlayedFighterManager().playerManager.id
        CurrentPlayedFighterManager().setCharacteristicsInformations(self._playerId, self._stats)
        PlayedCharacterUpdatesFrame.updateCharacterStatsList(self._stats, True)
        SpellWrapper.refreshAllPlayerSpellHolder(self._playerId)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._playerId]

    def displayDetailedStatsDifferences(
        self,
        oldStat: CharacterCharacteristicDetailed,
        newStat: CharacterCharacteristicDetailed,
    ) -> str:
        characterBaseCharacteristicChangeDetails: str = ""
        if newStat.base != oldStat.base:
            characterBaseCharacteristicChangeDetails += (
                "\r        - base : " + str(oldStat.base) + " -> " + str(newStat.base)
            )
        if newStat.additional != oldStat.additional:
            characterBaseCharacteristicChangeDetails += (
                "\r        - additional : " + str(oldStat.additional) + " -> " + str(newStat.additional)
            )
        if newStat.objectsAndMountBonus != oldStat.objectsAndMountBonus:
            characterBaseCharacteristicChangeDetails += (
                "\r        - objectsAndMountBonus : "
                + str(oldStat.objectsAndMountBonus)
                + " , "
                + str(newStat.objectsAndMountBonus)
            )
        if newStat.alignGiftBonus != oldStat.alignGiftBonus:
            characterBaseCharacteristicChangeDetails += (
                "\r        - alignGiftBonus : " + str(oldStat.alignGiftBonus) + " -> " + str(newStat.alignGiftBonus)
            )
        if newStat.contextModif != oldStat.contextModif:
            characterBaseCharacteristicChangeDetails += (
                "\r        - contextModif : " + str(oldStat.contextModif) + " -> " + str(newStat.contextModif)
            )
        return characterBaseCharacteristicChangeDetails
