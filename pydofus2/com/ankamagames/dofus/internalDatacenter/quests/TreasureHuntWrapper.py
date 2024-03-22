from typing import List

from pydofus2.com.ankamagames.dofus.internalDatacenter.quests.TreasureHuntStepWrapper import \
    TreasureHuntStepWrapper
from pydofus2.com.ankamagames.dofus.network.enums.TreasureHuntFlagStateEnum import \
    TreasureHuntFlagStateEnum
from pydofus2.com.ankamagames.dofus.network.enums.TreasureHuntTypeEnum import \
    TreasureHuntTypeEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntFlag import \
    TreasureHuntFlag
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStep import \
    TreasureHuntStep
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStepFight import \
    TreasureHuntStepFight
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStepFollowDirection import \
    TreasureHuntStepFollowDirection
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStepFollowDirectionToHint import \
    TreasureHuntStepFollowDirectionToHint
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStepFollowDirectionToPOI import \
    TreasureHuntStepFollowDirectionToPOI
from pydofus2.com.ankamagames.dofus.types.enums.TreasureHuntStepTypeEnum import \
    TreasureHuntStepTypeEnum
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum


class TreasureHuntWrapper(IDataCenter):
    def __init__(self):
        self.questType = 0
        self.checkPointCurrent = 0
        self.checkPointTotal = 0
        self.totalStepCount = 0
        self.availableRetryCount = 0
        self.stepList = list[TreasureHuntStepWrapper]()

    @classmethod
    def create(
        cls,
        questType: int,
        startMapId: float,
        checkPointCurrent: int,
        checkPointTotal: int,
        totalStepCount: int,
        availableRetryCount: int,
        stepList: List[TreasureHuntStep],
        flags: List[TreasureHuntFlag],
    ) -> "TreasureHuntWrapper":
        item = cls()
        item.questType = questType
        item.checkPointCurrent = checkPointCurrent
        item.checkPointTotal = checkPointTotal
        item.totalStepCount = totalStepCount
        item.availableRetryCount = availableRetryCount
        startStep = TreasureHuntStepWrapper.create(TreasureHuntStepTypeEnum.START, 0, 0, startMapId, 0)
        item.stepList.append(startStep)
        for i, step in enumerate(stepList):
            mapId = 0
            flagState = -1
            if flags and len(flags) > i and flags[i]:
                mapId = flags[i].mapId
                flagState = int(flags[i].state)
            if isinstance(step, TreasureHuntStepFollowDirectionToPOI):
                item.stepList.append(
                    TreasureHuntStepWrapper.create(
                        TreasureHuntStepTypeEnum.DIRECTION_TO_POI,
                        i,
                        step.direction,
                        mapId,
                        step.poiLabelId,
                        flagState,
                    )
                )
            elif isinstance(step, TreasureHuntStepFollowDirection):
                item.stepList.append(
                    TreasureHuntStepWrapper.create(
                        TreasureHuntStepTypeEnum.DIRECTION,
                        i,
                        step.direction,
                        mapId,
                        0,
                        flagState,
                        step.mapCount,
                    )
                )
            elif isinstance(step, TreasureHuntStepFollowDirectionToHint):
                item.stepList.append(
                    TreasureHuntStepWrapper.create(
                        TreasureHuntStepTypeEnum.DIRECTION_TO_HINT,
                        i,
                        step.direction,
                        mapId,
                        0,
                        flagState,
                        step.npcId,
                    )
                )
        while len(item.stepList) <= totalStepCount:
            item.stepList.append(TreasureHuntStepWrapper.create(TreasureHuntStepTypeEnum.UNKNOWN, 63, 0, 0, 0))
        item.stepList.append(TreasureHuntStepWrapper.create(TreasureHuntStepTypeEnum.FIGHT, 63, 0, 0, 0))
        return item

    def update(
        self,
        questType: int,
        startMapId: float,
        checkPointCurrent: int,
        checkPointTotal: int,
        availableRetryCount: int,
        stepList: List[TreasureHuntStep],
        flags: List[TreasureHuntFlag],
    ):
        self.questType = questType
        self.checkPointCurrent = checkPointCurrent
        self.checkPointTotal = checkPointTotal
        self.totalStepCount = checkPointTotal
        self.availableRetryCount = availableRetryCount
        self.stepList = list[TreasureHuntStep]()
        startStep = TreasureHuntStepWrapper.create(TreasureHuntStepTypeEnum.START, 0, 0, startMapId, 0)
        self.stepList.append(startStep)
        for i, step in enumerate(stepList):
            mapId = 0
            flagState = -1
            if flags and len(flags) > i and flags[i]:
                mapId = flags[i].mapId
                flagState = int(flags[i].state)
            if isinstance(step, TreasureHuntStepFollowDirectionToPOI):
                self.stepList.append(
                    TreasureHuntStepWrapper.create(
                        TreasureHuntStepTypeEnum.DIRECTION_TO_POI,
                        i,
                        step.direction,
                        mapId,
                        step.poiLabelId,
                        flagState,
                    )
                )
            elif isinstance(step, TreasureHuntStepFollowDirectionToHint):
                self.stepList.append(
                    TreasureHuntStepWrapper.create(
                        TreasureHuntStepTypeEnum.DIRECTION_TO_HINT,
                        i,
                        step.direction,
                        mapId,
                        0,
                        flagState,
                    )
                )
            elif isinstance(step, TreasureHuntStepFight):
                self.stepList.append(TreasureHuntStepWrapper.create(TreasureHuntStepTypeEnum.FIGHT, 63, 0, 0, 0))

    def __repr__(self) -> str:
        from prettytable import PrettyTable

        summaryTable = PrettyTable()
        summaryTable.field_names = [
            "questType",
            "checkPointCurrent",
            "checkPointTotal",
            "totalStepCount",
            "availableRetryCount",
        ]
        summaryTable.add_row(
            [
                TreasureHuntTypeEnum.to_string(self.questType),
                self.checkPointCurrent,
                self.checkPointTotal,
                self.totalStepCount,
                self.availableRetryCount,
            ]
        )
        stepsTable = PrettyTable()
        stepsTable.field_names = ["Type", "Index", "Direction", "Map ID", "POI Id", "Flag State", "NpcId"]
        for step in self.stepList:
            stepsTable.add_row(
                [
                    TreasureHuntStepTypeEnum.to_string(step.type),
                    step.index,
                    DirectionsEnum(step.direction).name,
                    step.mapId,
                    step.poiLabel,
                    TreasureHuntFlagStateEnum.to_string(step.flagState),
                    step.count,
                ]
            )
        return f"{summaryTable}\n{stepsTable}"
