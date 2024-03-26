import sys
from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff as basicBuff
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import \
    SpellLevel
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import \
    SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
    CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdProtocol import \
    ActionIdProtocol
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellBuff import \
    SpellBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import \
    StatBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StateBuff import \
    StateBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.TriggeredBuff import \
    TriggeredBuff
from pydofus2.com.ankamagames.dofus.logic.game.misc.StatBuffFactory import \
    StatBuffFactory
from pydofus2.com.ankamagames.dofus.misc.utils.GameDebugManager import \
    GameDebugManager
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.AbstractFightDispellableEffect import \
    AbstractFightDispellableEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostEffect import \
    FightTemporaryBoostEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostStateEffect import \
    FightTemporaryBoostStateEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostWeaponDamagesEffect import \
    FightTemporaryBoostWeaponDamagesEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporarySpellBoostEffect import \
    FightTemporarySpellBoostEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporarySpellImmunityEffect import \
    FightTemporarySpellImmunityEffect
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTriggeredEffect import \
    FightTriggeredEffect
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.types.CastingSpell import \
        CastingSpell


class BuffManager(metaclass=Singleton):

    INCREMENT_MODE_SOURCE: int = 1
    INCREMENT_MODE_TARGET: int = 2

    def __init__(self):
        self._buffs = dict[int, list[basicBuff.BasicBuff]]()
        self.spellBuffsToIgnore = list["CastingSpell"]()
        super().__init__()

    @classmethod
    def makeBuffFromEffect(
        cls,
        effect: AbstractFightDispellableEffect,
        castingSpell: "CastingSpell",
        actionId: int,
    ) -> basicBuff.BasicBuff:
        criticalEffect: bool = False
        if GameDebugManager().buffsDebugActivated:
            Logger().debug("[BUFFS DEBUG] Creation du buff " + str(effect.uid))

        if isinstance(effect, FightTemporarySpellBoostEffect):
            buff = SpellBuff(effect, castingSpell, actionId)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug("[BUFFS DEBUG]      Buff " + str(effect.uid) + " : type SpellBuff")

        if isinstance(effect, FightTriggeredEffect):
            buff = TriggeredBuff(effect, castingSpell, actionId)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug("[BUFFS DEBUG]      Buff " + str(effect.uid) + " : type TriggeredBuff")

        if isinstance(effect, FightTemporaryBoostWeaponDamagesEffect):
            ftbwde = effect
            buff = basicBuff.BasicBuff(
                effect,
                castingSpell,
                actionId,
                ftbwde.weaponTypeId,
                ftbwde.delta,
                ftbwde.weaponTypeId,
            )
            if GameDebugManager().buffsDebugActivated:
                Logger().debug(
                    "[BUFFS DEBUG]      Buff "
                    + str(effect.uid)
                    + " : type BasicBuff avec FightTemporaryBoostWeaponDamagesEffect"
                )

        if isinstance(effect, FightTemporaryBoostStateEffect):
            buff = StateBuff(effect, castingSpell, actionId)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug("[BUFFS DEBUG]      Buff " + str(effect.uid) + " : type StateBuff")

        if isinstance(effect, FightTemporarySpellImmunityEffect):
            ftsie = effect
            buff = basicBuff.BasicBuff(effect, castingSpell, actionId, ftsie.immuneSpellId, None, None)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug(
                    "[BUFFS DEBUG]      Buff "
                    + str(effect.uid)
                    + " : type BasicBuff avec FightTemporarySpellImmunityEffect"
                )

        if isinstance(effect, FightTemporaryBoostEffect):
            buff = StatBuffFactory.createStatBuff(effect, castingSpell, actionId)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug("[BUFFS DEBUG]      Buff " + str(effect.uid) + " : type StatBuff")

        buff.id = effect.uid
        spellLevelsId: int = -1
        spell: Spell = Spell.getSpellById(effect.spellId)
        level: SpellLevel = None
        for level in spell.spellLevelsInfo:
            for effectInstanceDice in level.effects:
                if effectInstanceDice.effectUid == effect.effectId:
                    spellLevelsId = level.id
            if spellLevelsId == -1:
                for effectInstanceDice in level.criticalEffect:
                    if effectInstanceDice.effectUid == effect.effectId:
                        spellLevelsId = level.id
                        criticalEffect = True
        if spellLevelsId != -1:
            spellLevel = SpellLevel.getLevelById(spellLevelsId)
            effects = spellLevel.effects if not criticalEffect else spellLevel.criticalEffect
            for effid in effects:
                if effid.effectUid == effect.effectId:
                    buff.effect.triggers = effid.triggers
                    buff.effect.targetMask = effid.targetMask
                    buff.effect.effectElement = effid.effectElement
            buff.castingSpell.spellRank = spellLevel
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(
                f"[BUFFS DEBUG]      Buff {effect.uid} : spell casted '{buff.castingSpell.spell.name}' ({buff.castingSpell.spell.id}) level {buff.castingSpell.spellRank.grade} by {buff.castingSpell.casterId}"
            )
        return buff

    def decrementDuration(self, targetId: float) -> None:
        self.incrementDuration(targetId, -1)

    def synchronize(self) -> None:
        if GameDebugManager().buffsDebugActivated:
            Logger().debug("[BUFFS DEBUG] Canceling disabled of all buffs")
        for entityId in self._buffs:
            for buffItem in self._buffs[entityId]:
                if buffItem.disabled:
                    buffItem.onReenable()

    def incrementDuration(
        self,
        targetId: float,
        delta: int,
        dispellEffect: bool = False,
        incrementMode: int = 1,
    ) -> None:
        modified: bool = False
        skipBuffUpdate: bool = False
        newBuffs: dict = dict[int, list]()
        for targetBuffs in self._buffs.values():
            for buffItem in targetBuffs:
                if dispellEffect and isinstance(buffItem, TriggeredBuff) and buffItem.delay > 0:
                    if newBuffs[buffItem.targetId] == None:
                        newBuffs[buffItem.targetId] = []
                    newBuffs[buffItem.targetId].append(buffItem)
                elif (
                    incrementMode == self.INCREMENT_MODE_SOURCE
                    and buffItem.aliveSource == targetId
                    or incrementMode == self.INCREMENT_MODE_TARGET
                    and buffItem.targetId == targetId
                ):
                    if incrementMode == self.INCREMENT_MODE_SOURCE and (
                        len(self.spellBuffsToIgnore) or buffItem.sourceJustReaffected
                    ):
                        skipBuffUpdate = False
                        for spell in self.spellBuffsToIgnore:
                            if (
                                spell.castingSpellId == buffItem.castingSpell.castingSpellId
                                and spell.casterId == targetId
                            ):
                                skipBuffUpdate = True
                        if buffItem.sourceJustReaffected:
                            skipBuffUpdate = True
                            buffItem.sourceJustReaffected = False
                        if skipBuffUpdate:
                            if newBuffs[buffItem.targetId] is None:
                                newBuffs[buffItem.targetId] = []
                            newBuffs[buffItem.targetId].append(buffItem)
                            continue
                    modified = buffItem.incrementDuration(delta, dispellEffect)
                    if buffItem.active:
                        if newBuffs.get(buffItem.targetId) is None:
                            newBuffs[buffItem.targetId] = []
                        newBuffs[buffItem.targetId].append(buffItem)
                        if modified:
                            pass
                    else:
                        buffItem.onRemoved()
                else:
                    if newBuffs.get(buffItem.targetId) is None:
                        newBuffs[buffItem.targetId] = []
                    newBuffs[buffItem.targetId].append(buffItem)
        self._buffs = newBuffs

    def markFinishingBuffs(self, targetId: float, currentTurnIsEnding: bool = True) -> None:
        fightBattleFrame = Kernel().battleFrame
        fightersCount = 0
        currentFighterId = CurrentPlayedFighterManager().currentFighterId
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(
                f"[BUFFS DEBUG] Looking for buffs of {targetId}"
                + " that will finish during the turn  (current fighter "
                + str(currentFighterId)
                + ") currentTurnIsEnding "
                + str(currentTurnIsEnding)
            )
        if targetId not in self._buffs:
            return
        for buffItem in self._buffs[targetId]:
            if buffItem.duration == 1:
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug(
                        "[BUFFS DEBUG]     - Buff "
                        + str(buffItem.uid)
                        + " n'a plus qu'un tour     (aliveSource "
                        + str(buffItem.aliveSource)
                        + "  sourceJustReaffected "
                        + str(buffItem.sourceJustReaffected)
                        + ")"
                    )
                buffWillEndBeforeTargetTurn = False
                casterIndex = -1
                targetIndex = -1
                currentFighterIndex = -1
                for i, fighterId in enumerate(fightBattleFrame.fightersList):
                    if fighterId == buffItem.aliveSource:
                        if buffItem.sourceJustReaffected:
                            buffItem.sourceJustReaffected = False
                        else:
                            casterIndex = i
                    if fighterId == buffItem.targetId:
                        targetIndex = i
                    if fighterId == currentFighterId:
                        currentFighterIndex = i
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug(
                        "[BUFFS DEBUG]             Index of fighters for this buff : caster "
                        + str(casterIndex)
                        + ", target "
                        + str(targetIndex)
                        + ", current fighter "
                        + str(currentFighterIndex)
                    )
                if casterIndex == -1 or targetIndex == -1 or currentFighterIndex == -1:
                    Logger().warn("Error when marking finishing buff, fighters cannot be found ")
                    return
                if casterIndex == targetIndex:
                    if currentFighterIndex == targetIndex and not currentTurnIsEnding:
                        if GameDebugManager().buffsDebugActivated:
                            Logger().debug(
                                "[BUFFS DEBUG]                 cible = target = combattant actuel et ce n'est pas une fin de tour, on ne desactive pas"
                            )
                        continue
                    buffWillEndBeforeTargetTurn = True
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug("[BUFFS DEBUG]                 cible = target, the buff must be disabled")
                elif currentFighterIndex == targetIndex and currentTurnIsEnding:
                    buffWillEndBeforeTargetTurn = True
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(
                            "[BUFFS DEBUG]                 end of the target turn, the buff must be disabled"
                        )
                else:
                    if casterIndex > targetIndex:
                        if currentFighterIndex >= casterIndex:
                            currentFighterIndex -= fightersCount
                        casterIndex -= fightersCount
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(
                            "[BUFFS DEBUG]           --->  Index of fighters for this buff : caster "
                            + str(casterIndex)
                            + ", target "
                            + str(targetIndex)
                            + ", current fighter "
                            + str(currentFighterIndex)
                        )
                    if currentFighterIndex < casterIndex or currentFighterIndex > targetIndex:
                        buffWillEndBeforeTargetTurn = True
                        if GameDebugManager().buffsDebugActivated:
                            Logger().debug(
                                "[BUFFS DEBUG]                 le combattant actuel n'est pas entre le caster et la target, le buff doit etre desactiv�"
                            )
                if buffWillEndBeforeTargetTurn:
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(
                            "[BUFFS DEBUG]                   Buff "
                            + str(buffItem.uid)
                            + " should be deactivated, should not be shown amongs the stats of the fighter"
                        )
                    buffItem.onDisabled()

    def addBuff(self, buff: basicBuff.BasicBuff, applyBuff: bool = True) -> None:
        if buff.targetId not in self._buffs:
            self._buffs[buff.targetId] = []
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(f"[BUFFS DEBUG] Ajout du buff {buff.uid} sur {buff.targetId}")
        sameBuff = None
        for actualBuff in self._buffs[buff.targetId]:
            if buff == actualBuff:
                sameBuff = actualBuff
                break
        if (
            not sameBuff
            or buff.actionId == ActionIds.ACTION_CHARACTER_BOOST_THRESHOLD
            or buff.actionId == ActionIds.ACTION_SET_SPELL_RANGE_MAX
            or buff.actionId == ActionIds.ACTION_SET_SPELL_RANGE_MIN
            or buff.actionId == ActionIds.ACTION_INHERITE_CHARAC
        ):
            self._buffs[buff.targetId].append(buff)
        else:
            if (
                isinstance(sameBuff, TriggeredBuff)
                and "|" in sameBuff.effect.triggers
                or sameBuff.castingSpell.spellRank
                and sameBuff.castingSpell.spellRank.maxStack
                and len(sameBuff.stack) == sameBuff.castingSpell.spellRank.maxStack
            ):
                return
            sameBuff.add(buff)
        if applyBuff:
            buff.onApplied()
        if not sameBuff:
            KernelEventsManager().send(KernelEvent.BuffAdd, buff.id, buff.targetId)
        else:
            KernelEventsManager().send(KernelEvent.BuffUpdate, sameBuff.id, sameBuff.targetId)

    def updateBuff(self, buff: basicBuff.BasicBuff) -> bool:
        targetId: float = buff.targetId
        if GameDebugManager().buffsDebugActivated:
            Logger().debug("[BUFFS DEBUG] Mise � jour du buff " + str(buff.uid) + " sur " + str(buff.targetId))
        if not self._buffs[targetId]:
            return False
        i: int = self.getBuffIndex(targetId, buff.id)
        if i == -1:
            return False
        self._buffs[targetId][i].onRemoved()
        self._buffs[targetId][i].updateParam(buff.param1, buff.param2, buff.param3, buff.id)
        oldBuff = self._buffs[targetId][i]
        if not oldBuff:
            return False
        oldBuff.onApplied()
        return True

    def dispell(
        self,
        targetId: float,
        forceUndispellable: bool = False,
        critical: bool = False,
        dying: bool = False,
    ) -> None:
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(f"[BUFFS DEBUG] Desenvotment of all buffs belongin to {targetId}")
        newBuffs: list = []
        for buff in self._buffs.get(targetId, []):
            if buff.canBeDispell(forceUndispellable, -sys.maxsize + 1, dying):
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug("[BUFFS DEBUG]      Buff " + str(buff.uid) + " doit �tre retir�")
                buff.onRemoved()
            else:
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug("[BUFFS DEBUG]      Buff " + str(buff.uid) + " remains")
                newBuffs.append(buff)
        self._buffs[targetId] = newBuffs

    def dispellSpell(
        self,
        targetId: float,
        spellId: int,
        forceUndispellable: bool = False,
        critical: bool = False,
        dying: bool = False,
    ) -> None:
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(
                "[BUFFS DEBUG] Desenvoutement de tous les buffs du sort " + str(spellId) + " de " + str(targetId)
            )
        newBuffs: list = []
        currentFighterId: float = CurrentPlayedFighterManager().currentFighterId
        if targetId in self._buffs:
            for buff in self._buffs[targetId]:
                if spellId == buff.castingSpell.spell.id and buff.canBeDispell(
                    forceUndispellable, -sys.maxsize + 1, dying
                ):
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(f"[BUFFS DEBUG]      Buff {buff.uid} doit �tre retir�")
                    buff.onRemoved()
                else:
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(f"[BUFFS DEBUG]      Buff {buff.uid} reste")
                    newBuffs.append(buff)
        self._buffs[targetId] = newBuffs

    def dispellUniqueBuff(
        self,
        targetId: float,
        boostUID: int,
        forceUndispellable: bool = False,
        dying: bool = False,
        ultimateDebuff: bool = True,
    ) -> None:
        isState: bool = False
        i: int = self.getBuffIndex(targetId, boostUID)
        if i == -1:
            return
        buff: basicBuff.BasicBuff = self._buffs[targetId][i]
        if buff.canBeDispell(forceUndispellable, int(boostUID) if ultimateDebuff else -99999999, dying):
            if buff.stack and len(buff.stack) > 1 and not dying:
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug(
                        "[BUFFS DEBUG] Desenvoutement du buff stack� " + str(boostUID) + " de " + str(targetId)
                    )
                buff.onRemoved()
                isState = False
                if buff.actionId == ActionIds.ACTION_BOOST_SPELL_BASE_DMG:
                    buff.param1 = buff.stack[0].param1
                    buff.param2 -= buff.stack[0].param2
                    buff.param3 -= buff.stack[0].param3
                if buff.actionId == ActionIds.ACTION_CHARACTER_PUNISHMENT:
                    buff.param1 -= buff.stack[0].param2
                if (
                    buff.actionId == ActionIds.ACTION_FIGHT_SET_STATE
                    or buff.actionId == ActionIds.ACTION_FIGHT_UNSET_STATE
                ):
                    isState = True
                else:
                    buff.param1 -= buff.stack[0].param1
                    buff.param2 -= buff.stack[0].param2
                    buff.param3 -= buff.stack[0].param3
                buff.stack.pop(0)
                buff.refreshDescription()
                if not isState:
                    buff.onApplied()
            else:
                if GameDebugManager().buffsDebugActivated:
                    Logger().debug("[BUFFS DEBUG] Desenvoutement du buff " + str(boostUID) + " de " + str(targetId))
                self._buffs[targetId].remove(buff)
                buff.onRemoved()
                if targetId == CurrentPlayedFighterManager().currentFighterId:
                    SpellWrapper.refreshAllPlayerSpellHolder(targetId)

    def removeLinkedBuff(self, sourceId: float, forceUndispellable: bool = False, dying: bool = False) -> list:
        impactedTarget: list = []
        entitiesFrame = Kernel().fightEntitiesFrame
        infos = entitiesFrame.getEntityInfos(sourceId)
        if GameDebugManager().buffsDebugActivated:
            Logger().debug(f"[BUFFS DEBUG] Retrieving all the buffs casted by {sourceId}")
        for buffList in self._buffs.values():
            buffListCopy = buffList.copy()
            for buff in buffListCopy:
                if buff.source == sourceId:
                    if GameDebugManager().buffsDebugActivated:
                        Logger().debug(f"[BUFFS DEBUG] Buff {buff.uid} must be retrieved")
                    self.dispellUniqueBuff(buff.targetId, buff.id, forceUndispellable, dying, False)
                    if buff.targetId not in impactedTarget:
                        impactedTarget.append(buff.targetId)
                    if (
                        dying
                        and infos.stats.summoned
                        and infos.stats.summoner != CurrentPlayedFighterManager().currentFighterId
                    ):
                        buff.aliveSource = infos.stats.summoner
                        if GameDebugManager().buffsDebugActivated:
                            Logger().debug(
                                f"[BUFFS DEBUG] Buff {buff.uid} must be reaffected to the summoner {infos.stats.summoner}"
                            )
        return impactedTarget

    def reaffectBuffs(self, sourceId: float) -> None:
        entity: GameFightFighterInformations = self.fightEntitiesFrame.getEntityInfos(sourceId)
        if entity.stats.summoned:
            next = self.getNextFighter(sourceId)
            if GameDebugManager().buffsDebugActivated:
                Logger().debug(f"[BUFFS DEBUG] Reaffecting buffs casted by {sourceId}, the next caster is {next}")
            dontDecrementBuffThisTurn = False
            if CurrentPlayedFighterManager().currentFighterId == sourceId:
                dontDecrementBuffThisTurn = True
            for buffList in self._buffs.values():
                for buff in buffList:
                    if buff.aliveSource == sourceId:
                        if GameDebugManager().buffsDebugActivated:
                            Logger().debug(f"[BUFFS DEBUG] Buff {buff.uid} must be reaffected")
                        buff.aliveSource = next
                        buff.sourceJustReaffected = dontDecrementBuffThisTurn

    def getNextFighter(self, sourceId: float) -> float:
        frame = Kernel().battleFrame
        if frame is None:
            return 0
        found: bool = False
        for fighter in frame.fightersList:
            if found:
                return fighter
            if fighter == sourceId:
                found = True
        if found:
            return frame.fightersList[0]
        return 0

    def getFighterInfo(self, targetId: float) -> GameFightFighterInformations:
        return self.fightEntitiesFrame.getEntityInfos(targetId)

    def getAllBuff(self, targetId: float) -> list[StatBuff]:
        return self._buffs.get(targetId, [])

    def getLifeThreshold(self, targetId: float) -> int:
        targetBuffs: list = self._buffs[targetId]
        if not targetBuffs:
            return 0
        for index in range(len(targetBuffs)):
            buff = targetBuffs[index]
            if (
                buff
                and not buff.removed
                and buff.actionId == ActionIdProtocol.ACTION_CHARACTER_BOOST_THRESHOLD
                and isinstance(buff, StatBuff)
            ):
                lifeThreshold = max(lifeThreshold, buff)
        return lifeThreshold

    def resetTriggerCount(self, targetId: float) -> bool:
        for buff in self._buffs.get(targetId, []):
            if isinstance(buff, TriggeredBuff):
                buff.triggerCount = 0
                return True
        return False

    def getBuff(self, buffId: int, playerId: float) -> basicBuff.BasicBuff:
        for buff in self._buffs.get(playerId, []):
            if buffId == buff.id:
                return buff
        return None

    @property
    def fightEntitiesFrame(self):
        return Kernel().fightEntitiesFrame

    def getBuffIndex(self, targetId: float, buffId: int) -> int:
        for i, sbuff in enumerate(self._buffs.get(targetId, [])):
            if buffId == sbuff.id:
                return i
            for subBuff in sbuff.stack:
                if buffId == subBuff.id:
                    return i
        return -1
