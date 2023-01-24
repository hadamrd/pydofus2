from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.dofus.datacenter.interactives.Interactive import Interactive
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Skill import Skill
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.messages.InteractiveElementActivationMessage import (
    InteractiveElementActivationMessage,
)
from pydofus2.com.ankamagames.dofus.network.enums.MapObstacleStateEnum import MapObstacleStateEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import GameContextDestroyMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapObstacleUpdateMessage import (
    MapObstacleUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveElementUpdatedMessage import (
    InteractiveElementUpdatedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveMapUpdateMessage import (
    InteractiveMapUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUsedMessage import InteractiveUsedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseEndedMessage import (
    InteractiveUseEndedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.InteractiveUseErrorMessage import (
    InteractiveUseErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.StatedElementUpdatedMessage import (
    StatedElementUpdatedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.StatedMapUpdateMessage import StatedMapUpdateMessage
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElementSkill import InteractiveElementSkill
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.StatedElement import StatedElement
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import RoleplayEntitiesFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayMovementFrame import RoleplayMovementFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayWorldFrame import RoleplayWorldFrame

logger = Logger("Dofus2")


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


class InteractiveElementData:
    def __init__(self, element: InteractiveElement, position: MapPoint, skillUID: int) -> None:
        self.element = element
        self.position = position
        self.skillUID = skillUID


class RoleplayInteractivesFrame(Frame):

    COLLECTABLE_COLLECTING_STATE_ID: int = 2

    COLLECTABLE_CUT_STATE_ID: int = 1

    ACTION_COLLECTABLE_RESOURCES: int = 1

    _ie: dict[int, InteractiveElementData]

    _currentUsages: list

    _entities: dict

    _usingInteractive: bool = False

    _nextInteractiveUsed: object = None

    _interactiveActionTimers: dict

    _enableWorldInteraction: bool = True

    _collectableSpritesToBeStopped: dict

    _currentRequestedElementId: int = -1

    _currentUsedElementId: int = -1

    _collectableIe = dict[int, dict]()

    dirmov: int = 666

    REVIVE_SKILL_ID = 211

    def __init__(self):
        self._ie = dict[int, InteractiveElementData]()
        self._collectableIe = dict[int, CollectableElement]()
        self._currentUsages = list()
        self._entities = dict()
        self._interactiveActionTimers = dict()
        self._collectableSpritesToBeStopped = dict()
        self._statedElementsTargetAnimation = dict()
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def roleplayWorldFrame(self) -> "RoleplayWorldFrame":
        return Kernel().worker.getFrame("RoleplayWorldFrame")

    @property
    def movementFrame(self) -> "RoleplayMovementFrame":
        return Kernel().worker.getFrame("RoleplayMovementFrame")

    @property
    def currentRequestedElementId(self) -> int:
        return self._currentRequestedElementId

    @currentRequestedElementId.setter
    def currentRequestedElementId(self, pElementId: int) -> None:
        self._currentRequestedElementId = pElementId

    @property
    def usingInteractive(self) -> bool:
        return self._usingInteractive

    @usingInteractive.setter
    def usingInteractive(self, pUsing: bool) -> None:
        self._usingInteractive = pUsing

    @property
    def nextInteractiveUsed(self) -> object:
        return self._nextInteractiveUsed

    @nextInteractiveUsed.setter
    def nextInteractiveUsed(self, object: object) -> None:
        self._nextInteractiveUsed = object

    @property
    def worldInteractionIsEnable(self) -> bool:
        return self._enableWorldInteraction

    @property
    def interactives(self) -> dict[int, InteractiveElementData]:
        return self._ie

    @property
    def collectables(self) -> dict[int, CollectableElement]:
        return self._collectableIe

    def pushed(self) -> bool:
        # logger.debug("InteractiveElement pushed")
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
            if len(ieumsg.interactiveElement.enabledSkills):
                self.registerInteractive(
                    ieumsg.interactiveElement,
                    ieumsg.interactiveElement.enabledSkills[0].skillInstanceUid,
                )
            elif len(ieumsg.interactiveElement.disabledSkills):
                self.registerInteractive(
                    ieumsg.interactiveElement,
                    ieumsg.interactiveElement.disabledSkills[0].skillInstanceUid,
                )
            else:
                self.removeInteractive(ieumsg.interactiveElement)
            return True

        if isinstance(msg, InteractiveUsedMessage):
            iumsg = msg
            if PlayedCharacterManager().id == iumsg.entityId and iumsg.duration > 0:
                self._currentUsedElementId = iumsg.elemId
            if self._currentRequestedElementId == iumsg.elemId:
                self._currentRequestedElementId = -1
            if iumsg.duration > 0:
                if PlayedCharacterManager().id == iumsg.entityId:
                    self._usingInteractive = True
                    rwf = self.roleplayWorldFrame
                    if rwf:
                        rwf.cellClickEnabled = False
                self._entities[iumsg.elemId] = iumsg.entityId
                if (
                    self.movementFrame
                    and self.movementFrame._followingIe
                    and self.movementFrame._followingIe["ie"].elementId == iumsg.elemId
                ):
                    self.movementFrame.cancelFollowingIe()
                logger.debug(
                    f"[RolePlayInteractives] Interactive element {iumsg.elemId} is being used by the Entity '{'CurrentPlayer' if iumsg.entityId == PlayedCharacterManager().id else iumsg.entityId}'"
                )
            return False

        if isinstance(msg, InteractiveUseErrorMessage):
            iuem = msg
            if iuem.elemId == self._currentRequestedElementId:
                self._currentRequestedElementId = -1
            return False

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
            moumsg = msg
            for mo in moumsg.obstacles:
                InteractiveCellManager().updateCell(
                    mo.obstacleCellId, mo.state == MapObstacleStateEnum.OBSTACLE_OPENED
                )
            return True

        if isinstance(msg, InteractiveUseEndedMessage):
            iuemsg = msg
            self.interactiveUsageFinished(self._entities[iuemsg.elemId], iuemsg.elemId, iuemsg.skillId)
            del self._entities[iuemsg.elemId]
            del self._collectableIe[iuemsg.elemId]
            return False

        if isinstance(msg, GameContextDestroyMessage):
            return False

        return False

    def pulled(self) -> bool:
        self._entities.clear()
        self._ie.clear()
        self._currentUsages.clear()
        self._nextInteractiveUsed = None
        self._interactiveActionTimers.clear()
        self._collectableIe.clear()
        # logger.debug("InteractiveElement pulled")
        return True

    def enableWorldInteraction(self, pEnable: bool) -> None:
        self._enableWorldInteraction = pEnable

    def clear(self) -> None:
        self._ie.clear()
        self._collectableIe.clear()

    def getInteractiveElementsCells(self) -> list[int]:
        cells = [cellObj.position.cellId for cellObj in self._ie.values() if cellObj is not None]
        return cells

    def getInteractiveActionTimer(self, pUser) -> BenchmarkTimer:
        return self._interactiveActionTimers[pUser]

    def getInteractiveElement(self, elementId: int, skillId=None) -> InteractiveElementData:
        ie = self._ie.get(elementId)
        if skillId is not None and ie is not None:
            for skill in ie.element.enabledSkills:
                if skill.skillId == skillId:
                    ie.skillUID = skill.skillInstanceUid
        return ie

    def registerInteractive(self, ie: InteractiveElement, firstSkill: int) -> None:
        if not MapDisplayManager().isIdentifiedElement(ie.elementId):
            return
        entitiesFrame: "RoleplayEntitiesFrame" = Kernel().worker.getFrame("RoleplayEntitiesFrame")
        if entitiesFrame:
            found = False
            for s, cie in enumerate(entitiesFrame.interactiveElements):
                if cie.elementId == ie.elementId:
                    found = True
                    entitiesFrame.interactiveElements[int(s)] = ie
            if not found:
                entitiesFrame.interactiveElements.append(ie)
        worldPos: MapPoint = MapDisplayManager().getIdentifiedElementPosition(ie.elementId)
        self._ie[ie.elementId] = InteractiveElementData(ie, worldPos, firstSkill)

    def removeInteractive(self, ie: InteractiveElement) -> None:
        if self._ie.get(ie.elementId):
            del self._ie[ie.elementId]

    def isCollectable(self, ie: InteractiveElement) -> CollectableElement:
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

    def getIeBySkillId(self, skillId: int) -> InteractiveElementData:
        for ie in self._ie.values():
            if ie.element.enabledSkills:
                for skill in ie.element.enabledSkills:
                    if skill.skillId == skillId:
                        ie.skillUID = skill.skillInstanceUid
                        return ie

    def getNearestIeToPosition(self, position: MapPoint, skillId: int) -> InteractiveElementData:
        minDist = float("inf")
        target = None
        for ie in self._ie.values():
            if ie.element.enabledSkills:
                for skill in ie.element.enabledSkills:
                    if skill.skillId == skillId:
                        dist = position.distanceTo(ie.position)
                        if dist < minDist:
                            dist = minDist
                            target = ie
                            target.skillUID = skill.skillInstanceUid
        return target

    def updateStatedElement(self, se: StatedElement, globalv: bool = False) -> None:
        if se.elementId == self._currentUsedElementId:
            self._usingInteractive = True
        if se.elementId in self._ie and self._ie[se.elementId].element.onCurrentMap:
            collectable = self.isCollectable(self._ie[se.elementId].element)
            if collectable is not None:
                self._collectableIe[collectable.id] = collectable

    def canBeCollected(self, elementId: int) -> CollectableElement:
        return self._collectableIe.get(elementId)

    def skillClicked(self, ie: InteractiveElementData) -> None:
        msg: InteractiveElementActivationMessage = InteractiveElementActivationMessage(
            ie.element, ie.position, ie.skillUID
        )
        Kernel().worker.process(msg)

    def interactiveUsageFinished(self, entityId: float, elementId: int, skillId: int) -> None:
        if entityId == PlayedCharacterManager().id:
            if self.roleplayWorldFrame:
                self.roleplayWorldFrame.cellClickEnabled = True
            self._usingInteractive = False
            self._currentUsedElementId = -1
            if self._nextInteractiveUsed:
                ieamsg = InteractiveElementActivationMessage(
                    self._nextInteractiveUsed.ie,
                    self._nextInteractiveUsed.position,
                    self._nextInteractiveUsed.skillInstanceId,
                )
                self._nextInteractiveUsed = None
                Kernel().worker.process(ieamsg)
