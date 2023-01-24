from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from whistle import Event
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDice import (
    EffectInstanceDice,
)
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.fightEvents.FightEvent import FightEvent
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import StatBuff

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
        FightEntitiesFrame,
    )
    from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import BasicBuff
from pydofus2.com.ankamagames.dofus.misc.utils.GameDebugManager import GameDebugManager
from pydofus2.com.ankamagames.dofus.network.enums.FightEventEnum import FightEventEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.utils.display.EnterFrameConst import EnterFrameConst
from pydofus2.com.ankamagames.jerakine.utils.display.EnterFrameDispatcher import (
    EnterFrameDispatcher,
)

logger = Logger()


class FightEventsHelper(metaclass=Singleton):

    _fightEvents: list[FightEvent] = list[FightEvent]()

    _events: list[list[FightEvent]] = list[list[FightEvent]]()

    _joinedEvents: list[FightEvent] = list[FightEvent]()

    _detailsActive: bool = False

    _lastSpellId: int = -1

    NOT_GROUPABLE_BY_TYPE_EVENTS: list = [FightEventEnum.FIGHTER_CASTED_SPELL]

    SKIP_ENTITY_ALIVE_CHECK_EVENTS: list = [
        FightEventEnum.FIGHTER_GOT_KILLED,
        FightEventEnum.FIGHTER_DEATH,
    ]

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self._fightEvents = list[FightEvent]()
        self._events = list[list[FightEvent]]()
        self._joinedEvents = list[FightEvent]()
        self._lastSpellId = -1

    def sendFightEvent(
        self,
        name: str,
        params: list,
        fighterId: float,
        pCastingSpellId: int,
        sendNow: bool = False,
        checkParams: int = 0,
        pFirstParamToCheck: int = 1,
        buff: "BasicBuff" = None,
    ) -> None:
        fightEvent: FightEvent = FightEvent(
            name,
            params,
            fighterId,
            checkParams,
            pCastingSpellId,
            len(self._fightEvents),
            pFirstParamToCheck,
            buff,
        )
        if sendNow:
            pass
        else:
            if name:
                self._fightEvents.insert(0, fightEvent)
            if self._joinedEvents and len(self._joinedEvents) > 0:
                if self._joinedEvents[0].name == FightEventEnum.FIGHTER_GOT_TACKLED:
                    if name == FightEventEnum.FIGHTER_MP_LOST or name == FightEventEnum.FIGHTER_AP_LOST:
                        self._joinedEvents.insert(0, fightEvent)
                        return
                    if name != FightEventEnum.FIGHTER_VISIBILITY_CHANGED:
                        feTackle = self._joinedEvents.pop(0)
                        for fe in self._joinedEvents:
                            if fe.name == FightEventEnum.FIGHTER_AP_LOST:
                                feTackle.params[1] = fe.params[1]
                            else:
                                feTackle.params[2] = fe.params[1]
                        self.addFightText(feTackle)
                        self._joinedEvents = None
            elif name == FightEventEnum.FIGHTER_GOT_TACKLED:
                self._joinedEvents = list[FightEvent]()
                self._joinedEvents.append(fightEvent)
                return
            if name:
                self.addFightText(fightEvent)

    def addFightText(self, fightEvent: FightEvent) -> None:
        num: int = len(self._events)
        targetEvent = None
        groupByType = fightEvent.name not in self.NOT_GROUPABLE_BY_TYPE_EVENTS
        if GameDebugManager().detailedFightLog_unGroupEffects:
            groupByType = False
        if fightEvent.name == FightEventEnum.FIGHTER_CASTED_SPELL:
            self._lastSpellId = fightEvent.params[3]
        if (
            fightEvent.name == FightEventEnum.FIGHTER_LIFE_LOSS
            or fightEvent.name == FightEventEnum.FIGHTER_LIFE_GAIN
            or fightEvent.name == FightEventEnum.FIGHTER_SHIELD_LOSS
        ):
            fightEvent.params.append(self._lastSpellId)
        if fightEvent.name == FightEventEnum.FIGHTER_LIFE_LOSS:
            for i in range(num):
                event = self._events[i][0]
                if (
                    event.name == FightEventEnum.FIGHTER_REDUCED_DAMAGES
                    and event.castingSpellId == fightEvent.castingSpellId
                    and event.targetId == fightEvent.targetId
                ):
                    groupByType = False
                    break
        if groupByType:
            for i in range(num):
                eventList = self._events[i]
                event = eventList[0]
                if event.name == fightEvent.name and (
                    event.castingSpellId == fightEvent.castingSpellId or fightEvent.castingSpellId == -1
                ):
                    if (
                        event.name == FightEventEnum.FIGHTER_LIFE_LOSS
                        or fightEvent.name == FightEventEnum.FIGHTER_LIFE_GAIN
                        or fightEvent.name == FightEventEnum.FIGHTER_SHIELD_LOSS
                    ) and event.params[len(event.params) - 1] != fightEvent.params[len(fightEvent.params) - 1]:
                        break
                    targetEvent = eventList
                    break
        if targetEvent == None:
            targetEvent = list[FightEvent]()
            self._events.append(targetEvent)
        targetEvent.append(fightEvent)

    def sendAllFightEvent(self, now: bool = False) -> None:
        if now:
            self.sendEvents(None)
        else:
            EnterFrameDispatcher().addEventListener(self.sendEvents, EnterFrameConst.SEND_FIGHT_EVENTS_HELPER)

    def sendEvents(self, pEvt: Event = None) -> None:
        EnterFrameDispatcher().removeEventListener(self.sendEvents)
        self.sendFightEvent(None, None, 0, -1)
        self.sendAllFightEvents()
        entitiesFrame: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
        entitiesList: dict = entitiesFrame.entities if entitiesFrame else dict()
        self.groupAllEventsForDisplay(entitiesList)

    def groupAllEventsForDisplay(self, entitiesList: dict) -> None:
        playerTeamId: int = PlayedCharacterManager().teamId
        deadTargetsDescr: object = self.getDeadTargetsDescr()
        deadTargets: dict = deadTargetsDescr["deadTargets"]
        lastDamageMap: dict = deadTargetsDescr["lastDamageMap"]
        eventsGroupedByTarget: dict = dict()
        groupedByElementsEventList = None
        while len(self._events) > 0:
            eventList = self._events[0]
            if eventList is None or len(eventList) == 0:
                self._events.pop(0)
            else:
                eventBase = eventList[0]
                targetsId = self.extractTargetsId(eventList)
                eventsGroupedByTarget = self.groupFightEventsByTarget(eventList)
                eventsGroupedTargets = list[str]()
                for targetEvents in eventsGroupedByTarget:
                    if len(eventsGroupedByTarget[targetEvents]):
                        eventsGroupedTargets.insert(0, targetEvents)
                    else:
                        eventsGroupedTargets.append(targetEvents)
                numTargets = len(eventsGroupedTargets)
                for i in range(numTargets):
                    targetEvents = eventsGroupedTargets[i]
                    eventBase = eventsGroupedByTarget[targetEvents][0]
                    if len(eventsGroupedByTarget[targetEvents]) > 1 and (
                        eventBase.name == FightEventEnum.FIGHTER_LIFE_LOSS
                        or eventBase.name == FightEventEnum.FIGHTER_LIFE_GAIN
                        or eventBase.name == FightEventEnum.FIGHTER_SHIELD_LOSS
                    ):
                        if (
                            eventBase.name == FightEventEnum.FIGHTER_LIFE_LOSS
                            or eventBase.name == FightEventEnum.FIGHTER_SHIELD_LOSS
                        ):
                            typeEvent = -1
                        if eventBase.name == FightEventEnum.FIGHTER_LIFE_GAIN:
                            typeEvent = 1
                        else:
                            typeEvent = 1
                        fightEvent = self.groupByElements(
                            eventsGroupedByTarget[targetEvents],
                            typeEvent,
                            self._detailsActive,
                            deadTargets[eventBase.targetId],
                            eventBase.castingSpellId,
                        )
                        if not groupedByElementsEventList:
                            groupedByElementsEventList = list[FightEvent]()
                        groupedByElementsEventList.append(fightEvent)
                        for tmpevt in eventsGroupedByTarget[targetEvents]:
                            eventList.remove(tmpevt)
                    else:
                        ecopy = eventList.copy()
                        for eventBase in ecopy:
                            if eventBase.name == FightEventEnum.FIGHTER_DEATH and deadTargets[eventBase.targetId]:
                                eventList.remove(eventBase)
                        self.groupByTeam(
                            playerTeamId,
                            targetsId,
                            eventList,
                            entitiesList,
                            deadTargets,
                        )
                        ecopy = eventList.copy()
                        for eventBase in ecopy:
                            isLastDamage = (
                                eventBase.name == FightEventEnum.FIGHTER_LIFE_LOSS
                                and lastDamageMap[eventBase.targetId] == eventBase.id
                                and deadTargets[eventBase.targetId]
                            )
                            eventList.remove(eventBase)
                        ecopy = None
                if groupedByElementsEventList and len(groupedByElementsEventList) > 0:
                    self.groupByTeam(
                        playerTeamId,
                        targetsId,
                        groupedByElementsEventList,
                        entitiesList,
                        deadTargets,
                        False,
                    )
                    if len(groupedByElementsEventList) > 0:
                        for fightEvent in groupedByElementsEventList:
                            pass
                    groupedByElementsEventList = None

    def extractTargetsId(self, eventList: list[FightEvent]) -> list[float]:
        event: FightEvent = None
        targetList: list[float] = list[float]()
        for event in eventList:
            if event.targetId not in targetList:
                targetList.append(event.targetId)
        return targetList

    def groupFightEventsByTarget(self, eventList: list[FightEvent]) -> dict:
        event: FightEvent = None
        dico: dict = dict[str, list]()
        for event in eventList:
            if dico.get(str(event.targetId)) is None:
                dico[str(event.targetId)] = list()
            dico[str(event.targetId)].append(event)
        return dico

    def getDeadTargetsDescr(self) -> object:
        deadTargets: dict = dict()
        lastDamageMap: dict = dict()
        events: list[list[FightEvent]] = self._events.copy()
        for eventList in events:
            for fightEvent in eventList:
                if fightEvent.name == FightEventEnum.FIGHTER_LIFE_LOSS and not deadTargets.get(fightEvent.targetId):
                    lastDamageMap[fightEvent.targetId] = fightEvent.id
                elif fightEvent.name == FightEventEnum.FIGHTER_DEATH:
                    deadTargets[fightEvent.targetId] = True
        return {"deadTargets": deadTargets, "lastDamageMap": lastDamageMap}

    def groupByElements(
        self,
        pvgroup: list[FightEvent],
        pType: int,
        activeDetails: bool = True,
        pAddDeathInTheSameMsg: bool = False,
        pCastingSpellId: int = -1,
    ) -> FightEvent:
        ttptsStr: str = ""
        for fe in pvgroup:
            if not (pCastingSpellId != -1 and pCastingSpellId != fe.castingSpellId):
                if previousElement and fe.params[2] != previousElement:
                    pass
                fe.params[2]
                fe.params[1]
        fightEventName = "fightLifeLossAndDeath" if pAddDeathInTheSameMsg else pvgroup[0].name
        newparams: list = list()
        newparams[0] = pvgroup[0].params[0]
        if activeDetails and len(pvgroup) > 1:
            fightEventText += "</b> (" + ttptsStr[0, len(ttptsStr) - 3] + ")<b>"
        newparams[1] = fightEventText
        return FightEvent(
            fightEventName,
            newparams,
            newparams[0],
            2,
            pvgroup[0].castingSpellId,
            len(pvgroup),
            1,
        )

    def groupByTeam(
        self,
        playerTeamId: int,
        targets: list[float],
        pEventList: list[FightEvent],
        pEntitiesList: dict,
        deadTargets: dict,
        pEnableColoration: bool = True,
    ) -> bool:
        if len(pEventList) == 0:
            return False
        tmpEventList: list[FightEvent] = pEventList
        while len(tmpEventList) > 1:
            listToConcat = self.getGroupedListEvent(tmpEventList)
            if len(listToConcat) <= 1:
                continue
            elist = list[float]()
            for event in listToConcat:
                elist.append(event.targetId)
                if (
                    event != listToConcat[0]
                    and event.targetId == listToConcat[0].targetId
                    and isinstance(listToConcat[0], StatBuff)
                ):
                    listToConcat[0].params[1] += event.params[1]
            evt = listToConcat[0]
            if isinstance(evt.buff, StatBuff):
                tmpEffect = evt.buff.effect.clone()
                if isinstance(tmpEffect, EffectInstanceDice):
                    buffStackCount = 1
                    tmpDiceNum = int(evt.buff.rawParam1)
                    for event in listToConcat:
                        if event.targetId == evt.targetId and event.buff.id != evt.buff.id:
                            if (
                                evt.buff.castingSpell.spellRank.maxStack
                                and buffStackCount >= evt.buff.castingSpell.spellRank.maxStack
                            ):
                                break
                            buffStackCount += 1
                            tmpDiceNum += int(event.buff.rawParam1)
                    EffectInstanceDice(tmpEffect).diceNum = tmpDiceNum
                evt.params[1] = tmpEffect.description
            team = self.groupEntitiesByTeam(
                playerTeamId,
                elist,
                pEntitiesList,
                (pEventList[0].name not in self.SKIP_ENTITY_ALIVE_CHECK_EVENTS) if pEventList else False,
            )
            if team in ["all", "allies", "enemies"]:
                self.removeEventFromEventsList(pEventList, listToConcat)
                if evt.name == "fighterLifeLoss" and deadTargets[listToConcat[0].targetId]:
                    pass
            elif team == "other":
                self.removeEventFromEventsList(pEventList, listToConcat)
            if team == "none":
                logger.warn("Failed to group FightEvents for the team 'none'")
            else:
                for t in pEntitiesList.values():
                    if isinstance(t, GameFightFighterInformations):
                        teamId = t.spawnInfo.teamId
                    else:
                        teamId = t.teamId
                    if (
                        "allies" in team
                        and teamId == playerTeamId
                        or "enemies" in team
                        and teamId != playerTeamId
                    ):
                        if t.contextualId in elist:
                            elist.remove(t.contextualId)
                self.removeEventFromEventsList(pEventList, listToConcat)
                if evt.name == "fighterLifeLoss" and deadTargets[listToConcat[0].targetId]:
                    pass
                else:
                    pass
        return False

    def getGroupedListEvent(self, pInEventList: list[FightEvent]) -> list[FightEvent]:
        baseEvent: FightEvent = pInEventList[0]
        listToConcat: list[FightEvent] = list[FightEvent]()
        listToConcat.append(baseEvent)
        for event in pInEventList:
            if event not in listToConcat and self.needToGroupFightEventsData(
                self.getNumberOfParametersToCheck(baseEvent), event, baseEvent
            ):
                listToConcat.append(event)
        self.removeEventFromEventsList(pInEventList, listToConcat)
        return listToConcat

    def removeEventFromEventsList(self, pEventList: list[FightEvent], pListToRemove: list[FightEvent]) -> None:
        event: FightEvent = None
        for event in pListToRemove:
            if event in pEventList:
                pEventList.remove(event)

    def groupEntitiesByTeam(
        self,
        playerTeamId: int,
        targetList: list[float],
        entitiesList: dict,
        checkAlive: bool = True,
    ) -> str:
        fighterInfos: GameFightFighterInformations = None
        returnData = None
        alliesCount: int = 0
        enemiesCount: int = 0
        nbTotalAllies: int = 0
        nbTotalEnemies: int = 0
        for fighterInfos in entitiesList.values():
            if fighterInfos != None:
                if fighterInfos.spawnInfo.teamId == playerTeamId:
                    nbTotalAllies += 1
                else:
                    nbTotalEnemies += 1
                if (
                    not checkAlive or checkAlive and fighterInfos.spawnInfo.alive
                ) and fighterInfos.contextualId in targetList:
                    if fighterInfos.spawnInfo.teamId == playerTeamId:
                        alliesCount += 1
                    else:
                        enemiesCount += 1
        returnData = ""
        if nbTotalAllies == alliesCount and nbTotalEnemies == enemiesCount:
            return "all"
        if alliesCount > 1 and alliesCount == nbTotalAllies:
            returnData += ("," if returnData != "" else "") + "allies"
            if enemiesCount > 0 and enemiesCount < nbTotalEnemies:
                returnData += ",other"
        if enemiesCount > 1 and enemiesCount == nbTotalEnemies:
            returnData += ("," if returnData != "" else "") + "enemies"
            if alliesCount > 0 and alliesCount < nbTotalAllies:
                returnData += ",other"
        if returnData == "" and len(targetList) > 1:
            returnData += ("," if returnData != "" else "") + "other"
        return "none" if returnData == "" else returnData

    def getNumberOfParametersToCheck(self, baseEvent: FightEvent) -> int:
        numParam: int = len(baseEvent.params)
        if numParam > baseEvent.checkParams:
            numParam = baseEvent.checkParams
        return numParam

    def needToGroupFightEventsData(self, pNbParams: int, pFightEvent: FightEvent, pBaseEvent: FightEvent) -> bool:
        if (
            pFightEvent.castingSpellId != pBaseEvent.castingSpellId
            or GameDebugManager().detailedFightLog_unGroupEffects
            or pFightEvent.buff
            and pFightEvent.buff.disabled != pBaseEvent.buff.disabled
        ):
            return False
        for paramId in range(pFightEvent.firstParamToCheck, pNbParams):
            if pFightEvent.params[paramId] != pBaseEvent.params[paramId]:
                return False
        return True

    def sendAllFightEvents(self) -> None:
        self.clearData()

    def clearData(self) -> None:
        self._fightEvents = list[FightEvent]()
        FightEvent.reset()

    @property
    def fightEvents(self) -> list[FightEvent]:
        return self._fightEvents

    @property
    def events(self) -> list[list[FightEvent]]:
        return self._events

    @property
    def joinedEvents(self) -> list[FightEvent]:
        return self._joinedEvents
