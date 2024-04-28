from pydofus2.com.ankamagames.dofus.logic.game.fight.types.FighterStatus import FighterStatus
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton


class FightersStateManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._entityStates = dict[float, dict[int, float]]()

    def addStateOnTarget(self, targetId: float, stateId: int, delta: int = 1) -> None:
        targetKey = float(targetId)
        statKey = int(stateId)
        if not self._entityStates.get(targetKey):
            self._entityStates[targetKey] = dict()

        if not self._entityStates[targetKey].get(statKey):
            self._entityStates[targetKey][statKey] = delta

        else:
            self._entityStates[targetKey][statKey] += delta

    def removeStateOnTarget(self, targetId: float, stateId: int, delta: int = 1) -> None:
        targetKey = float(targetId)
        statKey = int(stateId)
        if not self._entityStates.get(targetKey):
            Logger().error(f"Can't find state list for {targetKey} to remove state")
            return

        if self._entityStates[targetKey].get(statKey):
            self._entityStates[targetKey][statKey] -= delta
            if self._entityStates[targetKey][statKey] == 0:
                del self._entityStates[targetKey][statKey]

    def hasState(self, targetId: float, stateId: int) -> bool:
        targetKey = float(targetId)
        statKey = int(stateId)
        if not self._entityStates.get(targetKey) or not self._entityStates[targetKey].get(statKey):
            return False
        return self._entityStates[targetKey][statKey] > 0

    def getStates(self, targetId: float) -> list:
        targetKey = float(targetId)
        stateId = None
        states: list = list()
        if targetKey not in self._entityStates:
            return states

        for stateId in self._entityStates[targetKey]:
            if self._entityStates[targetKey][stateId] > 0:
                states.append(stateId)

        return states

    def getStatus(self, targetId: float) -> FighterStatus:
        from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellState import SpellState

        targetKey = float(targetId)
        fighterstatus: FighterStatus = FighterStatus()
        for stateId in self._entityStates.get(targetKey, {}):
            state = SpellState.getSpellStateById(stateId)
            if state and self._entityStates[targetKey][stateId] > 0:
                if state.preventsSpellCast:
                    fighterstatus.cantUseSpells = True

                if state.preventsFight:
                    fighterstatus.cantUseCloseQuarterAttack = True

                if state.cantDealDamage:
                    fighterstatus.cantDealDamage = True

                if state.invulnerable:
                    fighterstatus.invulnerable = True

                if state.incurable:
                    fighterstatus.incurable = True

                if state.cantBeMoved:
                    fighterstatus.cantBeMoved = True

                if state.cantBePushed:
                    fighterstatus.cantBePushed = True

                if state.cantSwitchPosition:
                    fighterstatus.cantSwitchPosition = True

                if state.invulnerableMelee:
                    fighterstatus.invulnerableMelee = True

                if state.invulnerableRange:
                    fighterstatus.invulnerableRange = True

                if state.cantTackle:
                    fighterstatus.cantTackle = True

                if state.cantBeTackled:
                    fighterstatus.cantBeTackled = True

        return fighterstatus

    def endFight(self) -> None:
        self._entityStates.clear()
