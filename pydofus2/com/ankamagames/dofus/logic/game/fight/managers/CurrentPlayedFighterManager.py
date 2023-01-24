from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.dofus.network.enums.CharacterSpellModificationTypeEnum import CharacterSpellModificationTypeEnum
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
    from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import (
        SpellWrapper,
    )
import pydofus2.com.ankamagames.dofus.kernel.Kernel as knl
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellCastInFightManager as scifm
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import (
    SpellManager,
)
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import (
    CharacterCharacteristicsInformations,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

# from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellState import SpellState
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import (
    FightersStateManager,
)
import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.damageCalculation.tools.StatIds import StatIds
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter

logger = Logger("Dofus2")


class CurrentPlayedFighterManager(metaclass=Singleton):

    _currentFighterId: float = 0

    _currentFighterIsRealPlayer: bool = True

    _characteristicsInformationsList: dict

    _spellCastInFightManagerList: dict

    _currentSummonedCreature: dict

    _currentSummonedBomb: dict

    def __init__(self):
        self._characteristicsInformationsList = dict()
        self._spellCastInFightManagerList = dict()
        self._currentSummonedCreature = dict()
        self._currentSummonedBomb = dict()
        super().__init__()

    @property
    def currentFighterId(self) -> float:
        return self._currentFighterId

    @currentFighterId.setter
    def currentFighterId(self, id: float) -> None:
        if id == self._currentFighterId:
            return
        lastFighterId: float = self._currentFighterId
        self._currentFighterId = id
        playerManager = pcm.PlayedCharacterManager()
        self._currentFighterIsRealPlayer = self._currentFighterId == playerManager.id
        lastFighterEntity: "AnimatedCharacter" = DofusEntities.getEntity(lastFighterId)
        if lastFighterEntity:
            lastFighterEntity.canSeeThrough = False
            lastFighterEntity.canWalkThrough = False
            lastFighterEntity.canWalkTo = False
        currentFighterEntity: "AnimatedCharacter" = DofusEntities.getEntity(self._currentFighterId)
        if currentFighterEntity:
            currentFighterEntity.canSeeThrough = True
            currentFighterEntity.canWalkThrough = True
            currentFighterEntity.canWalkTo = True
        if playerManager.isFighting:
            if playerManager.id != id or lastFighterId:
                pass

    def checkPlayableEntity(self, id: float) -> bool:
        if id == pcm.PlayedCharacterManager().id:
            return True
        return self._characteristicsInformationsList.get(id) != None

    def isRealPlayer(self) -> bool:
        return self._currentFighterIsRealPlayer

    def resetPlayerSpellList(self) -> None:
        playerManager = pcm.PlayedCharacterManager()
        # inventoryManager:InventoryManager = InventoryManager()
        if playerManager.spellsInventory != playerManager.playerSpellList:
            logger.info("Remise à jour de la liste des sorts du joueur")
            playerManager.spellsInventory = playerManager.playerSpellList
            if knl.Kernel().worker.contains("FightSpellCastFrame"):
                knl.Kernel().worker.removeFrame(knl.Kernel().worker.getFrame("FightSpellCastFrame"))

    def setCharacteristicsInformations(self, id: float, characteristics: CharacterCharacteristicsInformations) -> None:
        self._characteristicsInformationsList[id] = characteristics

    def getCharacteristicsInformations(self, id: float = 0) -> CharacterCharacteristicsInformations:
        player = pcm.PlayedCharacterManager()
        if id:
            if id == player.id:
                return player.characteristics
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
        player = pcm.PlayedCharacterManager()
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

    def canCastThisSpell(self, spellId: int, lvl: int, pTargetId: float = 0, result: list = None) -> bool:
        from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell

        spellName = None
        spell: Spell = Spell.getSpellById(spellId)
        spellLevel: SpellLevel = spell.getSpellLevel(lvl)
        if spellLevel == None:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.noSpell", [spellName])
            return False
        player = pcm.PlayedCharacterManager()
        if self._currentFighterIsRealPlayer:
            if spellId == 0:
                if player.currentWeapon:
                    spellName = player.currentWeapon.name
                else:
                    spellName = spell.name
            else:
                spellName = "{spell," + str(spellId) + "," + str(lvl) + "}"
            if spellLevel.minPlayerLevel > player.infos.level:
                if result:
                    if player.infos.level > ProtocolConstantsEnum.MAX_LEVEL:
                        result[0] = I18n.getUiText(
                            "ui.fightAutomsg.spellcast.prestigeTooLow",
                            [spellName, player.infos.level - ProtocolConstantsEnum.MAX_LEVEL],
                        )
                    else:
                        result[0] = I18n.getUiText(
                            "ui.fightAutomsg.spellcast.levelTooLow", [spellName, player.infos.level]
                        )
                return False
            characteristics = self.getCharacteristicsInformations()
            if not characteristics:
                if result:
                    result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.notAvailableWithoutStats", [spellName])
                return False
        selfSpell = None
        for spellKnown in player.spellsInventory:
            if spellKnown and spellKnown.id == spellId:
                selfSpell = spellKnown
                break
        if not selfSpell:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.notAvailable", [spellName])
            return False
        entityStats: EntityStats = StatsManager().getStats(self.currentFighterId)
        currentPA: int = int(entityStats.getStatTotalValue(StatIds.ACTION_POINTS)) if entityStats is not None else 0
        if spellId == 0 and player.currentWeapon is not None:
            weapon = Item.getItemById(player.currentWeapon.objectGID)
            if not weapon:
                if result:
                    result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.notAWeapon", [spellName])
                return False
            apCost = weapon.apCost
            maxCastPerTurn = weapon.maxCastPerTurn
        else:
            apCost = selfSpell["apCost"]
            maxCastPerTurn = selfSpell["maxCastPerTurn"]
        if apCost > currentPA:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.needAP", [spellName, apCost])
            return False
        states: list = FightersStateManager().getStates(self._currentFighterId)
        if not states:
            states = list()
        for state in states:
            currentState = SpellState.getSpellStateById(state)
            if currentState.preventsFight and spellId == 0:
                if result:
                    result[0] = I18n.getUiText(
                        "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                    )
                return False
            if currentState.id == DataEnum.SPELL_STATE_ARCHER and spellId == 0:
                weapon2 = Item.getItemById(player.currentWeapon.objectGID)
                if weapon2.typeId != DataEnum.ITEM_TYPE_BOW:
                    if result:
                        result[0] = I18n.getUiText(
                            "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                        )
                    return False
            if currentState.preventsSpellCast:
                if not spellLevel.statesCriterion or spellLevel.statesCriterion == "":
                    if result:
                        result[0] = I18n.getUiText(
                            "ui.fightAutomsg.spellcast.stateForbidden", [spellName, currentState.name]
                        )
                    return False
                criterion = GroupItemCriterion(spellLevel.statesCriterion)
                isRequired = False
                for requiredStateCriterion in criterion.criteria:
                    if isinstance(requiredStateCriterion, StateCriterion) and  requiredStateCriterion.operatorText == ItemCriterionOperator.EQUAL:
                        if int(requiredStateCriterion.criterionValue == currentState.id):
                            isRequired = True
                            break
                if not isRequired:
                    break
            gic = GroupItemCriterion(spellLevel.statesCriterion)
            if not gic.isRespected:
                if result:
                    result[0] = I18n.getUiText(
                        "ui.fightAutomsg.spellcast.notAvailable", [spellName]
                    )
                return False
        if not spell.bypassSummoningLimit and spellLevel.canSummon and not self.canSummon():
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.tooManySummon", [spellName])
            return False
        if spellLevel.canBomb and not self.canBomb():
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.tooManyBomb", [spellName])
            return False
        if not player.isFighting:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
            return True
        spellCastManager: scifm.SpellCastInFightManager = self.getSpellCastManager()
        spellManager: SpellManager = spellCastManager.getSpellManagerBySpellId(spellId)
        if spellManager is None:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
            return True
        if maxCastPerTurn <= spellManager.numberCastThisTurn and maxCastPerTurn > 0:
            if result:
                result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.castPerTurn", [spellName, maxCastPerTurn])
            return False
        if spellManager.cooldown > 0 or selfSpell.actualCooldown > 0:
            cooldown = max(spellManager.cooldown, selfSpell.actualCooldown)
            if result:
                if cooldown == 63:
                    result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.noCast", [spellName])
                else:
                    result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.cooldown", [spellName, cooldown])
            return False
        if pTargetId != 0:
            numberCastOnTarget = spellManager.getCastOnEntity(pTargetId)
            spellModifiers = SpellModifiersManager().getSpellModifiers(self.currentFighterId, spellId)
            bonus = (
                float(spellModifiers.getModifierValue(CharacterSpellModificationTypeEnum.MAX_CAST_PER_TARGET))
                if not not spellModifiers
                else float(0)
            )
            if spellLevel.maxCastPerTarget + bonus <= numberCastOnTarget and spellLevel.maxCastPerTarget > 0:
                if result:
                    result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.castPerTarget", [spellName])
                return False
        if result:
            result[0] = I18n.getUiText("ui.fightAutomsg.spellcast.available", [spellName])
        return True

    def endFight(self) -> None:
        if pcm.PlayedCharacterManager().id != self._currentFighterId:
            self.currentFighterId = pcm.PlayedCharacterManager().id
            self.resetPlayerSpellList()
            # self.updatePortrait(DofusEntities.getEntity(self._currentFighterId))
        self._currentFighterId = 0
        self._characteristicsInformationsList = dict()
        self._spellCastInFightManagerList = dict()
        self._currentSummonedCreature = dict()
        self._currentSummonedBomb = dict()

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
