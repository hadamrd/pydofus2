from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntFlag import (
        TreasureHuntFlag,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.treasureHunt.TreasureHuntStep import (
        TreasureHuntStep,
    )


class TreasureHuntMessage(NetworkMessage):
    questType: int
    startMapId: int
    knownStepsList: list["TreasureHuntStep"]
    totalStepCount: int
    checkPointCurrent: int
    checkPointTotal: int
    availableRetryCount: int
    flags: list["TreasureHuntFlag"]

    def init(
        self,
        questType_: int,
        startMapId_: int,
        knownStepsList_: list["TreasureHuntStep"],
        totalStepCount_: int,
        checkPointCurrent_: int,
        checkPointTotal_: int,
        availableRetryCount_: int,
        flags_: list["TreasureHuntFlag"],
    ):
        self.questType = questType_
        self.startMapId = startMapId_
        self.knownStepsList = knownStepsList_
        self.totalStepCount = totalStepCount_
        self.checkPointCurrent = checkPointCurrent_
        self.checkPointTotal = checkPointTotal_
        self.availableRetryCount = availableRetryCount_
        self.flags = flags_

        super().__init__()
