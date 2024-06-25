from typing import Tuple

from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.interactives.Interactive import Interactive
from pydofus2.com.ankamagames.dofus.datacenter.interactives.Sign import Sign
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Skill import Skill
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.InteractiveElementData import InteractiveElementData
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import (
    GameContextDestroyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapObstacleUpdateMessage import (
    MapObstacleUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveElementUpdatedMessage import (
    InteractiveElementUpdatedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveMapUpdateMessage import (
    InteractiveMapUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import (
    InteractiveUsedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseEndedMessage import (
    InteractiveUseEndedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseErrorMessage import (
    InteractiveUseErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.StatedElementUpdatedMessage import (
    StatedElementUpdatedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.StatedMapUpdateMessage import (
    StatedMapUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElementSkill import (
    InteractiveElementSkill,
)
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.StatedElement import StatedElement
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class CollectableElement:
    def __init__(self, id: int, interactiveSkill: InteractiveElementSkill, enabled: bool):
        self.id = id
        self.skill = Skill.getSkillById(interactiveSkill.skillId)
        self.skillName = self.skill.name
        self.interactiveSkill = interactiveSkill
        self.enabled = enabled

    def __str__(self):
        return "CollectableElement(id={}, skill={}, SkillUID={}, enabled={})".format(
            self.id,
            self.skillName,
            self.interactiveSkill.skillInstanceUid,
            self.enabled,
        )


class RoleplayInteractivesFrame(Frame):

    COLLECTABLE_COLLECTING_STATE_ID = 2

    COLLECTABLE_CUT_STATE_ID = 1

    ACTION_COLLECTABLE_RESOURCES = 1

    REVIVE_SKILL_ID = 211

    ZAAP_TYPEID = 16

    REQUEST_TIMEOUT = 10

    BANK_HINT_GFX = 401

    NDIRECTIONS = 8

    def __init__(self):
        self._usingInteractive: bool = False
        self._ie = dict[int, InteractiveElementData]()
        self._collectableResource = dict[int, CollectableElement]()
        self._enityUsingElement = dict()
        self._statedElm = []
        self.currentRequestedElementId: int = -1
        self._currentUsedElementId: int = -1
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def interactives(self) -> dict[int, InteractiveElementData]:
        return self._ie

    @property
    def collectables(self) -> dict[int, CollectableElement]:
        return self._collectableResource

    def pushed(self) -> bool:
        Logger().debug("RoleplayInteractivesFrame pushed")
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, InteractiveMapUpdateMessage):
            imumsg = msg
            self.clear()
            for ie in imumsg.interactiveElements:
                if ie.enabledSkills:
                    self.registerInteractive(ie, ie.enabledSkills[0].skillInstanceUid)
                elif ie.disabledSkills:
                    self.registerInteractive(ie, ie.disabledSkills[0].skillInstanceUid)
            return True

        if isinstance(msg, InteractiveElementUpdatedMessage):
            ieumsg = msg
            if len(ieumsg.interactiveElement.enabledSkills) > 0:
                self.registerInteractive(
                    ieumsg.interactiveElement,
                    ieumsg.interactiveElement.enabledSkills[0].skillInstanceUid,
                )
            elif len(ieumsg.interactiveElement.disabledSkills) > 0:
                self.registerInteractive(
                    ieumsg.interactiveElement,
                    ieumsg.interactiveElement.disabledSkills[0].skillInstanceUid,
                )
            else:
                self.removeInteractive(ieumsg.interactiveElement)
            KernelEventsManager().send(KernelEvent.InteractiveElemUpdate, ieumsg)
            return True

        if isinstance(msg, InteractiveUsedMessage):
            if msg.duration > 0:
                self._enityUsingElement[msg.elemId] = msg.entityId
                KernelEventsManager().send(KernelEvent.IElemBeingUsed, msg.entityId, msg.elemId)
                if msg.entityId == PlayedCharacterManager().id:
                    Logger().info(f"Player is using element {msg.elemId} ...")
                    self.usingInteractive = True
            else:
                if msg.entityId == PlayedCharacterManager().id:
                    Logger().info(f"Player used element {msg.elemId}")
                KernelEventsManager().send(KernelEvent.InteractiveElementUsed, msg.entityId, msg.elemId)
            return True

        if isinstance(msg, InteractiveUseEndedMessage):
            Logger().info(f"Interactive element {msg.elemId} used.")
            entityId = self._enityUsingElement.get(msg.elemId)
            if entityId == PlayedCharacterManager().id:
                self.usingInteractive = False
            del self._enityUsingElement[msg.elemId]
            del self._collectableResource[msg.elemId]
            KernelEventsManager().send(KernelEvent.InteractiveElementUsed, entityId, msg.elemId)
            return True

        if isinstance(msg, InteractiveUseErrorMessage):
            iuem = msg
            if iuem.elemId == self.currentRequestedElementId:
                self.currentRequestedElementId = -1
            Logger().error(f"Interactive use error for element: {iuem.elemId}")
            KernelEventsManager().send(KernelEvent.InteractiveUseError, msg.elemId)
            return True

        if isinstance(msg, StatedMapUpdateMessage):
            smumsg = msg
            self._usingInteractive = False
            for se in smumsg.statedElements:
                self.updateStatedElement(se, True)
            return True

        if isinstance(msg, StatedElementUpdatedMessage):
            seumsg = msg
            self.updateStatedElement(seumsg.statedElement)
            return True

        if isinstance(msg, MapObstacleUpdateMessage):
            pass
            # for mo in moumsg.obstacles:
            #     InteractiveCellManager().updateCell(
            #         mo.obstacleCellId, mo.state == MapObstacleStateEnum.OBSTACLE_OPENED
            #     )
            return True

        if isinstance(msg, GameContextDestroyMessage):
            return False

        return False

    def pulled(self) -> bool:
        self._enityUsingElement.clear()
        self._ie.clear()
        self._collectableResource.clear()
        self._statedElm.clear()
        return True

    def clear(self) -> None:
        self._ie.clear()
        self._collectableResource.clear()

    def getInteractiveElementsCells(self) -> list[int]:
        cells = [cellObj.position.cellId for cellObj in self._ie.values() if cellObj is not None]
        return cells

    def getInteractiveElement(self, elementId: int, skillId=None) -> InteractiveElementData:
        ie = self._ie.get(elementId)
        if not ie:
            return None
        interactive = Interactive.getInteractiveById(ie.element.elementTypeId)
        if interactive:
            Logger().debug(f"Found interactive {interactive.name}")
        if skillId is not None and ie is not None:
            for skill in ie.element.enabledSkills:
                if skill.skillId == skillId:
                    ie.skillUID = skill.skillInstanceUid
                    ie.skillId = skill.skillId
        return ie

    def registerInteractive(self, ie: InteractiveElement, firstSkill: int) -> None:
        if not MapDisplayManager().isIdentifiedElement(ie.elementId):
            return
        if Kernel().roleplayEntitiesFrame:
            found = False
            for s, cie in enumerate(Kernel().roleplayEntitiesFrame.interactiveElements):
                if cie.elementId == ie.elementId:
                    found = True
                    Kernel().roleplayEntitiesFrame.interactiveElements[int(s)] = ie
                    break
            if not found:
                Kernel().roleplayEntitiesFrame.interactiveElements.append(ie)
        else:
            Logger().error("Received interactiveElem register but no entities frame found")
        worldPos = MapDisplayManager().getIdentifiedElementPosition(ie.elementId)
        self._ie[ie.elementId] = InteractiveElementData(ie, worldPos, firstSkill)

    def removeInteractive(self, ie: InteractiveElement) -> None:
        if self._ie.get(ie.elementId):
            del self._ie[ie.elementId]

    def isCollectableResource(self, ie: InteractiveElement) -> CollectableElement:
        interactive = Interactive.getInteractiveById(ie.elementTypeId)
        if interactive is not None:
            for interactiveSkill in ie.enabledSkills:
                skill = Skill.getSkillById(interactiveSkill.skillId)
                if skill.elementActionId == self.ACTION_COLLECTABLE_RESOURCES:
                    return CollectableElement(ie.elementId, interactiveSkill, True)
            for interactiveSkill in ie.disabledSkills:
                skill = Skill.getSkillById(interactiveSkill.skillId)
                if skill.elementActionId == self.ACTION_COLLECTABLE_RESOURCES:
                    return CollectableElement(ie.elementId, interactiveSkill, False)
        return None

    def getReviveIe(self) -> InteractiveElementData:
        return self.getIeBySkillId(self.REVIVE_SKILL_ID)

    def getBankDoorIe(self) -> InteractiveElementData:
        ie = self.getIeBySkillId(DataEnum.SKILL_SIGN_HINT)
        if ie:
            sign = Sign.getSignById(ie.element.elementId)
            if sign:
                Logger().debug(f"Found sign with text : {sign.signText}")
                if sign._hint.gfx == self.BANK_HINT_GFX:
                    return ie
        return None

    def getZaapIe(self) -> InteractiveElementData:
        return self.getIeByTypeId(self.ZAAP_TYPEID)

    def getIeByTypeId(self, typeId: int) -> InteractiveElementData:
        for ie in self._ie.values():
            if ie.element.elementTypeId == typeId:
                return ie

    def getIeBySkillId(self, skillId: int) -> InteractiveElementData:
        for ie in self._ie.values():
            if ie.element.enabledSkills:
                for skill in ie.element.enabledSkills:
                    if skill.skillId == skillId:
                        ie.skillUID = skill.skillInstanceUid
                        return ie

    def updateStatedElement(self, se: StatedElement, globalv: bool = False) -> None:
        self._statedElm.append(se.elementId)
        if se.elementId == self._currentUsedElementId:
            self._usingInteractive = True
        if se.elementId in self._ie and self._ie[se.elementId].element.onCurrentMap:
            collectable = self.isCollectableResource(self._ie[se.elementId].element)
            if collectable is not None:
                self._collectableResource[collectable.id] = collectable

    def canBeCollected(self, elementId: int) -> CollectableElement:
        return self._collectableResource.get(elementId)

    @classmethod
    def is_exit_skill(cls, ie: InteractiveElement) -> bool:
        if ie.enabledSkills:
            for skill in ie.enabledSkills:
                if skill.skillId == DataEnum.SKILL_POINT_OUT_EXIT:
                    return True
        return False

    @classmethod
    def getNearestCellToIe(
        cls, ie: InteractiveElement, iePos: MapPoint, playerPos: MapPoint = None
    ) -> Tuple[MapPoint, bool]:
        forbiddenCellsIds = list()
        cells = MapDisplayManager().dataMap.cells
        dmp = DataMapProvider()
        sendInteractiveUseRequest = True
        if not playerPos:
            playerPos = PlayedCharacterManager().entity.position
        for i in range(8):
            mp = iePos.getNearestCellInDirection(i)
            if mp:
                cellData = cells[mp.cellId]
                forbidden = (not cellData.mov) or cellData.farmCell
                if not forbidden:
                    numWalkableCells = 8
                    for j in range(8):
                        mp2 = mp.getNearestCellInDirection(j)
                        if mp2 and (
                            not dmp.pointMov(mp2.x, mp2.y, True, mp.cellId)
                            or not dmp.pointMov(mp2.x - 1, mp2.y, True, mp.cellId)
                            and not dmp.pointMov(mp2.x, mp2.y - 1, True, mp.cellId)
                        ):
                            numWalkableCells -= 1
                    if not numWalkableCells:
                        forbidden = True
                if forbidden:
                    if not forbiddenCellsIds:
                        forbiddenCellsIds = []
                    forbiddenCellsIds.append(mp.cellId)
        ieCellData = cells[iePos.cellId]
        if ie:
            minimalRange = 63
            skills = ie.enabledSkills
            for skillForRange in skills:
                skillData = Skill.getSkillById(skillForRange.skillId)
                if skillData:
                    if not skillData.useRangeInClient:
                        minimalRange = 1
                    elif skillData.range < minimalRange:
                        minimalRange = skillData.range
        else:
            minimalRange = 1
        distanceElementToPlayer = iePos.distanceToCell(playerPos)
        if distanceElementToPlayer <= minimalRange and ((not ieCellData.mov) or ieCellData.farmCell):
            nearestCell = playerPos
        else:
            orientationToCell = iePos.advancedOrientationTo(playerPos)
            nearestCell = iePos.getNearestFreeCellInDirection(
                orientationToCell,
                DataMapProvider(),
                True,
                True,
                False,
                forbiddenCellsIds,
            )
            if minimalRange > 1:
                for _ in range(minimalRange - 1):
                    forbiddenCellsIds.append(nearestCell.cellId)
                    nearestCell = nearestCell.getNearestFreeCellInDirection(
                        nearestCell.advancedOrientationTo(playerPos, False),
                        DataMapProvider(),
                        True,
                        True,
                        False,
                        forbiddenCellsIds,
                    )
                    if not nearestCell or nearestCell.cellId == playerPos.cellId:
                        break
        if ie:
            if len(skills) == 1 and skills[0].skillId == DataEnum.SKILL_POINT_OUT_EXIT:
                nearestCell.cellId = playerPos.cellId
                sendInteractiveUseRequest = False
        if not nearestCell or nearestCell.cellId in forbiddenCellsIds:
            nearestCell = iePos
        return nearestCell, sendInteractiveUseRequest
