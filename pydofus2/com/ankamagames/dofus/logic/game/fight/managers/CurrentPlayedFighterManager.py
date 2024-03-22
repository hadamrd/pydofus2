from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import \
    GroupItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import \
    ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.StateCriterion import \
    StateCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import \
    SpellModifiersManager
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierTypeEnum import \
    SpellModifierTypeEnum
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import (
        SpellWrapper,
    )
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
    from pydofus2.com.ankamagames.dofus.datacenter.items.Weapon import Weapon

import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
import pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastInFightManager as scifm
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellState import \
    SpellState
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import \
    EntityStats
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import \
    StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import \
    FightersStateManager
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import \
    CharacterCharacteristicsInformations
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.damageCalculation.tools.StatIds import StatIds


class CurrentPlayedFighterManager(metaclass=Singleton):
    
    def __init__(self):
        self._characteristicsInformationsList = dict()
        self._spellCastInFightManagerList = dict()
        self._currentSummonedCreature = dict()
        self._currentSummonedBomb = dict()
        self._currentFighterIsRealPlayer: bool = True
        self._currentFighterId: float = 0
        self.playerManager = pcm.PlayedCharacterManager()
        self.conn = ConnectionsHandler()
        super().__init__()

    @property
    def currentFighterId(self) -> float:
        return self._currentFighterId

    def setCurrentFighterId(self, id: float) -> None:
        if id == self._currentFighterId:
            return
        lastFighterId = self._currentFighterId
        self._currentFighterId = id
        self._currentFighterIsRealPlayer = self._currentFighterId == self.playerManager.id
        lastFighterEntity: "AnimatedCharacter" = DofusEntities().getEntity(lastFighterId)
        if lastFighterEntity:
            lastFighterEntity.canSeeThrough = False
            lastFighterEntity.canWalkThrough = False
            lastFighterEntity.canWalkTo = False
        currentFighterEntity: "AnimatedCharacter" = DofusEntities().getEntity(self._currentFighterId)
        if currentFighterEntity:
            currentFighterEntity.canSeeThrough = True
            currentFighterEntity.canWalkThrough = True
            currentFighterEntity.canWalkTo = True
            
    @currentFighterId.setter
    def currentFighterId(self, id: float) -> None:
        self.setCurrentFighterId(id)

    def checkPlayableEntity(self, id: float) -> bool:
        if id == self.playerManager.id:
            return True
        return self._characteristicsInformationsList.get(id) != None

    def isRealPlayer(self) -> bool:
        return self._currentFighterIsRealPlayer

    def resetPlayerSpellList(self) -> None:
        if self.playerManager and self.playerManager.spellsInventory != self.playerManager.playerSpellList:
            Logger().info(f"Update the player list of spells.")
            self.playerManager.spellsInventory = self.playerManager.playerSpellList

    def setCharacteristicsInformations(self, id: float, characteristics: CharacterCharacteristicsInformations) -> None:
        self._characteristicsInformationsList[id] = characteristics

    def getCharacteristicsInformations(self, id: float = 0) -> CharacterCharacteristicsInformations:
        player = self.playerManager
        if id:
            if id == player.id:
                return player.characteristics
            Logger().warn(f"Get characteristics informations for an entity that is not the player.")
            return self._characteristicsInformationsList[id]
        if self._currentFighterIsRealPlayer or not player.isFighting:
            return player.characteristics
        return self._characteristicsInformationsList[self._currentFighterId]

    def getStats(self, targetId: float = None) -> EntityStats:
        if targetId is None:
            targetId = self._currentFighterId
        return StatsManager().getStats(targetId)

    def getBasicTurnDuration(self) -> int:
        apBase: float = None
        apAdditional: float = None
        apBonus: float = None
        mpBase: float = None
        mpAdditional: float = None
        mpBonus: float = None
        totalTurnDurationInSeconds: int = 15
        stats: EntityStats = self.getStats(self._currentFighterId)
        if stats:
            apBase = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            apAdditional = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            apBonus = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            mpBase = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            mpAdditional = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            mpBonus = stats.getStatBaseValue(StatIds.ACTION_POINTS)
            totalTurnDurationInSeconds += apBase + apAdditional + apBonus + mpBase + mpAdditional + mpBonus
        return totalTurnDurationInSeconds

    def getSpellById(self, spellId: int) -> "SpellWrapper":
        player = self.playerManager
        for spellKnown in player.spellsInventory:
            if spellKnown.id == spellId:
                return spellKnown
        return None

    def getSpellCastManager(self) -> scifm.SpellCastInFightManager:
        scm: scifm.SpellCastInFightManager = self._spellCastInFightManagerList.get(self._currentFighterId)
        if not scm:
            scm = scifm.SpellCastInFightManager(self._currentFighterId)
            self._spellCastInFightManagerList[self._currentFighterId] = scm
        return scm

    def getSpellCastManagerById(self, id: float) -> scifm.SpellCastInFightManager:
        scm: scifm.SpellCastInFightManager = self._spellCastInFightManagerList.get(id)
        if not scm:
            scm = scifm.SpellCastInFightManager(id)
            self._spellCastInFightManagerList[id] = scm
        return scm

    def canCastThisSpell(self, spellId: int, lvl: int, pTargetId: float = 0,) -> bool:
        from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import \
            Spell

        spellName = None
        spell = Spell.getSpellById(spellId)
        spellLevel = spell.getSpellLevel(lvl)
        if spellLevel is None:
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.noSpell", [spellName])
            return False, reason
        player = self.playerManager
        if player:
            if spellId == 0:
                if player.currentWeapon:
                    spellName = player.currentWeapon.name
                else:
                    spellName = spell.name
            else:
                spellName = f"{spell.name,{spellId},{lvl}}"
            # if spellLevel.minPlayerLevel > player.infos.level:
            #     if player.infos.level > ProtocolConstantsEnum.MAX_LEVEL:
            #         reason = I18n.getUiText(
            #             "ui.fightAutomsg.spellcast.prestigeTooLow",
            #             [spellName, player.infos.level - ProtocolConstantsEnum.MAX_LEVEL],
            #         )
            #     else:
            #         reason = I18n.getUiText(
            #             "ui.fightAutomsg.spellcast.levelTooLow", [spellName, player.infos.level]
            #         )
            #     return False, reason
            if not StatsManager().getStats(self.currentFighterId):
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.notAvailableWithoutStats", [spellName])
                return False, reason
        thisSpell = None
        for spellKnown in player.spellsInventory:
            if spellKnown and spellKnown.id == spellId:
                thisSpell = spellKnown
                break
        if not thisSpell:
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.notAvailable", [spellName])
            return False, reason
        entityStats = StatsManager().getStats(self.currentFighterId)
        currentPA = int(entityStats.getStatTotalValue(StatIds.ACTION_POINTS)) if entityStats is not None else 0
        if spellId == 0 and player.currentWeapon is not None:
            weapon : "Weapon" = Item.getItemById(player.currentWeapon.objectGID)
            if not weapon:
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.notAWeapon", [spellName])
                return False, reason
            apCost = weapon.apCost
            maxCastPerTurn = weapon.maxCastPerTurn
        else:
            apCost = thisSpell['apCost']
            maxCastPerTurn = thisSpell['maxCastPerTurn']
        if apCost > currentPA:
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.needAP", [spellName, apCost])
            return False, reason
        states: list = FightersStateManager().getStates(self.currentFighterId)
        if not states:
            states = list()
        for state in states:
            currentState = SpellState.getSpellStateById(state)
            if currentState.preventsFight and spellId == 0:
                reason = I18n.getUiText(
                    "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                )
                return False, reason
            if currentState.id == DataEnum.SPELL_STATE_ARCHER and spellId == 0:
                weapon2 = Item.getItemById(player.currentWeapon.objectGID)
                if weapon2.typeId != DataEnum.ITEM_TYPE_BOW:
                    reason = I18n.getUiText(
                        "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                    )
                    return False, reason
            if currentState.preventsSpellCast:
                if not spellLevel.statesCriterion or spellLevel.statesCriterion == "":
                    reason = I18n.getUiText(
                        "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                    )
                    return False, reason
                criterion = GroupItemCriterion(spellLevel.statesCriterion)
                isRequired = False
                for requiredStateCriterion in criterion.criteria:
                    if (
                        isinstance(requiredStateCriterion, StateCriterion)
                        and requiredStateCriterion.operatorText == ItemCriterionOperator.EQUAL
                    ):
                        if int(requiredStateCriterion.criterionValue == currentState.id):
                            isRequired = True
                            break
                if not isRequired:
                    break
            gic = GroupItemCriterion(spellLevel.statesCriterion)
            if not gic.isRespected:
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.notAvailable", [spellName])
                return False, reason
        if not spell.bypassSummoningLimit and spellLevel.canSummon and not self.canSummon():
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.tooManySummon", [spellName])
            return False, reason
        if spellLevel.canBomb and not self.canBomb():
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.tooManyBomb", [spellName])
            return False, reason
        if not player.isFighting:
            Logger().error(f"Cancast spell called but Player is not fighting!")
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
            return True, reason
        spellCastManager = self.getSpellCastManager()
        spellManager = spellCastManager.getSpellManagerBySpellId(spellId)
        if spellManager is None:
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
            return True, reason
        if maxCastPerTurn <= spellManager.numberCastThisTurn and maxCastPerTurn > 0:
            reason = I18n.getUiText("ui.fightAutomsg.spellcast.castPerTurn", [spellName, maxCastPerTurn])
            return False, reason
        if spellManager.cooldown > 0 or thisSpell.actualCooldown > 0:
            cooldown = max(spellManager.cooldown, thisSpell.actualCooldown)
            if cooldown == 63:
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.noCast", [spellName])
            else:
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.cooldown", [spellName, cooldown])
            return False, reason
        if pTargetId != 0:
            numberCastOnTarget = spellManager.getCastOnEntity(pTargetId)
            bonus = SpellModifiersManager().getModifiedInt(self.currentFighterId, spellId, SpellModifierTypeEnum.MAX_CAST_PER_TARGET)
            if spellLevel.maxCastPerTarget + bonus <= numberCastOnTarget and spellLevel.maxCastPerTarget > 0:
                reason = I18n.getUiText("ui.fightAutomsg.spellcast.castPerTarget", [spellName])
                return False, reason
        reason = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
        return True, reason

    def endFight(self) -> None:
        if self.playerManager.id != self.currentFighterId:
            self.currentFighterId = self.playerManager.id
            self.resetPlayerSpellList()
        self._currentFighterId = 0
        self._characteristicsInformationsList.clear()
        self._spellCastInFightManagerList.clear()
        self._currentSummonedCreature.clear()
        self._currentSummonedBomb.clear()

    def getCurrentSummonedCreature(self, id: float = None) -> int:
        if id is None:
            id = self._currentFighterId
        return self._currentSummonedCreature.get(id, 0)

    def setCurrentSummonedCreature(self, value: int, id: float = None) -> None:
        if id is None:
            id = self._currentFighterId
        self._currentSummonedCreature[id] = value

    def getCurrentSummonedBomb(self, id: float = 0) -> int:
        if not id:
            id = self._currentFighterId
        return self._currentSummonedBomb[id]

    def setCurrentSummonedBomb(self, value: int, id: float = 0) -> None:
        if not id:
            id = self._currentFighterId
        self._currentSummonedBomb[id] = value

    def resetSummonedCreature(self, id: float = None) -> None:
        self.setCurrentSummonedCreature(0, id)

    def addSummonedCreature(self, id: float = None) -> None:
        self.setCurrentSummonedCreature(self.getCurrentSummonedCreature(id) + 1, id)

    def removeSummonedCreature(self, id: float = None) -> None:
        if self.getCurrentSummonedCreature(id) > 0:
            self.setCurrentSummonedCreature(self.getCurrentSummonedCreature(id) - 1, id)

    def getMaxSummonedCreature(self, id: float = None) -> int:
        stats: EntityStats = self.getStats(id)
        if stats == None:
            return 0
        return stats.getStatTotalValue(StatIds.MAX_SUMMONED_CREATURES_BOOST) - stats.getStatAdditionalValue(
            StatIds.MAX_SUMMONED_CREATURES_BOOST
        )

    def canSummon(self, id: float = None) -> bool:
        return self.getMaxSummonedCreature(id) > self.getCurrentSummonedCreature(id)

    def resetSummonedBomb(self, id: float = 0) -> None:
        self.setCurrentSummonedBomb(0, id)

    def addSummonedBomb(self, id: float = 0) -> None:
        self.setCurrentSummonedBomb(self.getCurrentSummonedBomb(id) + 1, id)

    def removeSummonedBomb(self, id: float = 0) -> None:
        if self.getCurrentSummonedBomb(id) > 0:
            self.setCurrentSummonedBomb(self.getCurrentSummonedBomb(id) - 1, id)

    def canBomb(self, id: float = 0) -> bool:
        return self.getMaxSummonedBomb() > self.getCurrentSummonedBomb(id)

    def getMaxSummonedBomb(self) -> int:
        return 3
