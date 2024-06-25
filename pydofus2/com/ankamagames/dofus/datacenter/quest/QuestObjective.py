from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.quest.NpcMessage import NpcMessage
from pydofus2.com.ankamagames.dofus.datacenter.quest.objectives.QuestObjectiveParameters import (
    QuestObjectiveParameters,
)
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjectiveType import QuestObjectiveType
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.flash.geom.Point import Point

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStep import QuestStep


class QuestObjective(IDataCenter):

    MODULE: str = "QuestObjectives"

    id: int

    stepId: int

    typeId: int

    dialogId: int

    parameters: QuestObjectiveParameters

    coords: Point

    mapId: float

    _step: "QuestStep" = None

    _type: QuestObjectiveType = None

    _text: str = ""

    _dialog: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getQuestObjectiveById(cls, id: int) -> "QuestObjective":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuestObjectives(cls) -> list["QuestObjective"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def step(self) -> "QuestStep":
        from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStep import QuestStep

        if not self._step:
            self._step = QuestStep.getQuestStepById(self.stepId)
        return self._step

    @property
    def type(self) -> QuestObjectiveType:
        if not self._type:
            self._type = QuestObjectiveType.getQuestObjectiveTypeById(self.typeId)
        return self._type

    @property
    def text(self) -> str:
        if not self._text:
            Logger().warn("Unknown objective type " + self.typeId + ", cannot display specific, parametrized text.")
            self._text = self.type.name
        return self._text

    @property
    def dialog(self) -> str:
        if self.dialogId < 1:
            return ""
        if not self._dialog:
            self._dialog = NpcMessage.getNpcMessageById(self.dialogId).message
        return self._dialog

    idAccessors: IdAccessors = IdAccessors(getQuestObjectiveById, getQuestObjectives)
