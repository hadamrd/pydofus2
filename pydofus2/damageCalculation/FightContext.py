from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.Preview.MapTranslator import MapTranslator
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import ActionIdHelper
from pydofus2.damageCalculation.fighterManagement.HaxeFighter import HaxeFighter
from pydofus2.damageCalculation.fighterManagement.playerTypeEnum import PlayerTypeEnum
from pydofus2.mapTools import MapTools


class FightContext:
    def __init__(
        self,
        gameTurn,
        gameMap: MapTranslator,
        targetedCell,
        originalCaster: HaxeFighter,
        fighters: list[HaxeFighter] = None,
        fighterInitialPositions=None,
        inputPortalCellId=-1,
        debugMode=False,
    ):
        self.lastKilledDefenders = list[HaxeFighter]()
        self.lastKilledChallengers = list[HaxeFighter]()
        self.inMovement = False
        self.tempFighters = list[HaxeFighter]()
        self.gameTurn = gameTurn
        self.map = gameMap
        self.targetedCell = targetedCell
        self.originalCaster = originalCaster
        self.triggeredMarks = []
        self.inputPortalCellId = inputPortalCellId
        self.debugMode = debugMode
        self.fighters = fighters if fighters is not None else []

        if originalCaster not in self.fighters:
            self.fighters.append(originalCaster)

        if fighterInitialPositions is None:
            self.fighterInitialPositions = self.map.getFightersInitialPositions()
            for fighter in self.fighters:
                self.removeFighterCells(fighter.id)
        else:
            self.fighterInitialPositions = fighterInitialPositions

    def usingPortal(self) -> bool:
        return self.inputPortalCellId != -1

    def removeFighterCells(self, fighter_id: float) -> None:
        self.fighterInitialPositions = [
            fighter for fighter in self.fighterInitialPositions if fighter["id"] != fighter_id
        ]

    def isCellEmptyForMovement(self, param1: int) -> bool:
        for _loc4_ in self.fighters:
            if _loc4_.getCurrentPositionCell() == param1:
                return False

        _loc5_ = self.fighterInitialPositions.h
        while _loc5_ is not None:
            _loc6_ = _loc5_.item
            _loc5_ = _loc5_.next
            _loc7_ = _loc6_
            if int(_loc7_.cell) == param1:
                return False

        return self.map.isCellWalkable(param1)

    def getPortalBonus(self, param1):
        if not ActionIdHelper.isPortalBonus(param1):
            return 0

        _loc2_ = list(filter(lambda mark: mark.active, self.map.getMarks(4)))
        if len(_loc2_) == 0:
            return 0

        _loc3_ = 0
        _loc4_ = 0
        _loc5_ = 0
        _loc6_ = next((mark for mark in _loc2_ if mark.mainCell == self.inputPortalCellId), None)

        if _loc6_ is None:
            return 0

        currentPortal = _loc6_
        _loc2_ = list(filter(lambda mark: mark.teamId == currentPortal.teamId, _loc2_))
        _loc2_.remove(currentPortal)
        _loc2_ = PortalUtils.getPortalChainFromPortals(currentPortal, _loc2_)

        for _loc8_ in _loc2_:
            _loc7_ = MapTools.getDistance(_loc8_.mainCell, currentPortal.mainCell)
            for _loc11_ in _loc8_.associatedSpell.getEffects():
                if _loc11_.actionId == 1181:
                    _loc4_ = max(_loc4_, _loc11_.param3)
                    _loc5_ = max(_loc5_, _loc11_.param1)
            _loc3_ += _loc7_
            currentPortal = _loc8_

        return _loc4_ + _loc3_ * _loc5_

    def getLastKilledAlly(self, param1):
        if param1 == 0 and self.lastKilledChallengers and len(self.lastKilledChallengers) > 0:
            return self.lastKilledChallengers[0]
        elif param1 == 1 and self.lastKilledDefenders and len(self.lastKilledDefenders) > 0:
            return self.lastKilledDefenders[0]
        else:
            return self.map.getLastKilledAlly(param1)

    def getFreeId(self):
        _loc1_ = 1
        _loc2_ = False
        while not _loc2_:
            _loc2_ = True
            for _loc5_ in self.getEveryFighter():
                if _loc1_ == _loc5_.id:
                    _loc1_ += 1
                    _loc2_ = False
                    break
        return _loc1_

    def getFightersUpTo(self, param1, param2, param3, param4, param5):
        _loc6_ = []
        _loc7_ = None
        while True:
            param1 = MapTools.getNextCellByDirection(param1, param2)
            param3 -= 1
            param4 -= 1
            if param3 <= 0:
                _loc7_ = self.getFighterFromCell(param1)
                if _loc7_:
                    _loc6_.append(_loc7_)
                    param5 -= 1
            if not _loc7_ or not MapTools.isValidCellId(param1) or param4 <= 0 or param5 <= 0:
                break

        return _loc6_

    def getFightersFromZone(self, param1, param2, param3):
        if not MapTools.isValidCellId(param2) or not MapTools.isValidCellId(param3):
            return []

        _loc4_ = []
        _loc5_ = lambda fighter, shape: (
            shape == "A" or fighter.isAlive() and (not fighter.hasState(8) or shape == "a")
        ) and MapTools.isValidCellId(fighter.getBeforeLastSpellPosition())

        for _loc8_ in self.fighters:
            if _loc5_(_loc8_, param1.shape) and param1.isCellInZone(
                _loc8_.getBeforeLastSpellPosition(), param2, param3
            ):
                _loc4_.append(_loc8_)

        _loc9_ = self.fighterInitialPositions.h
        while _loc9_:
            _loc11_ = _loc9_.item
            _loc9_ = _loc9_.next
            if MapTools.isValidCellId(_loc11_.cell) and param1.isCellInZone(_loc11_.cell, param2, param3):
                _loc8_ = self.createFighterById(_loc11_.id)
                if _loc8_ and _loc5_(_loc8_, param1.shape):
                    _loc4_.append(_loc8_)

        return _loc4_

    def getFighterFromCell(self, param1, param2=False):
        for fighter in self.fighters:
            if (param2 and fighter.getCurrentPositionCell() == param1) or (
                not param2 and fighter.getBeforeLastSpellPosition() == param1
            ):
                return fighter

        for item in self.fighterInitialPositions:
            if item.cell == param1:
                return self.createFighterById(item.id)
        return None

    def getFighterCurrentSummonCount(self, param1):
        count = 0
        for fighter in self.getEveryFighter():
            if (
                fighter.id != param1.id
                and fighter.isAlive()
                and fighter.data.isSummon()
                and fighter.data.useSummonSlot()
                and fighter.data.getSummonerId() == param1.id
                and not fighter.isStaticElement
            ):
                count += 1
        return count

    def getFighterById(self, param1):
        for fighter in self.fighters:
            if fighter.id == param1:
                return fighter
        return self.createFighterById(param1)

    def getEveryFighter(self):
        for fighter_id in self.map.getEveryFighterId():
            self.getFighterById(fighter_id)
        return self.fighters

    def getCarriedFighterBy(self, param1):
        fighter_id = self.map.getCarriedFighterIdBy(param1)
        if fighter_id != 0:
            return self.getFighterById(fighter_id)
        return None

    def getAffectedFighters(self):
        def isAffected(fighter):
            for effect in fighter.totalEffects:
                if (
                    effect.damageRange
                    or effect.movement
                    or effect.attemptedApTheft
                    or effect.attemptedAmTheft
                    or effect.apStolen
                    or effect.amStolen
                    or effect.rangeLoss
                    or effect.rangeGain
                    or effect.summon
                    or effect.isSummoning
                    or effect.dispell
                    or effect.death
                ):
                    return True
            return False

        return list(filter(isAffected, self.fighters))

    def createFighterById(self, param1):
        fighter = self.map.getFighterById(param1)
        if fighter:
            self.fighters.append(fighter)
            self.removeFighterCells(fighter.id)
        return fighter

    def copy(self):
        new_context = FightContext(
            self.gameTurn,
            self.map,
            self.targetedCell,
            self.originalCaster,
            self.fighters,
            self.fighterInitialPositions,
        )
        new_context.triggeredMarks = self.triggeredMarks
        new_context.tempFighters = self.tempFighters
        new_context.debugMode = self.debugMode
        new_context.inputPortalCellId = self.inputPortalCellId
        return new_context

    def addLastKilledAlly(self, param1: HaxeFighter):
        target_list = self.lastKilledChallengers if param1.teamId == 0 else self.lastKilledDefenders
        insert_pos = 0

        if param1.playerType == PlayerTypeEnum.HUMAN:
            insert_pos = 0
        elif param1.playerType != PlayerTypeEnum.HUMAN:
            while insert_pos < len(target_list) and target_list[insert_pos].playerType == PlayerTypeEnum.HUMAN:
                insert_pos += 1
            if param1.playerType != PlayerTypeEnum.SIDEKICK:
                while insert_pos < len(target_list) and target_list[insert_pos].playerType == PlayerTypeEnum.SIDEKICK:
                    insert_pos += 1

        if param1.teamId == 0:
            self.lastKilledChallengers.insert(insert_pos, param1)
        else:
            self.lastKilledDefenders.insert(insert_pos, param1)
