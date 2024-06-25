from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import TransitionTypeEnum
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum


class Transition:

    _type: int

    _direction: int

    _skillId: int

    _criterion: str

    _transitionMapId: float

    _cell: int

    _id: int

    def __init__(
        self,
        type: int,
        direction: int,
        skillId: int,
        criterion: str,
        transitionMapId: float,
        cell: int,
        id: int,
    ):
        super().__init__()
        self._type = type
        self._direction = direction
        self._skillId = skillId
        self._criterion = criterion
        self._transitionMapId = transitionMapId
        self._cell = cell
        self._id = id

    @property
    def type(self) -> int:
        return self._type

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def skillId(self) -> int:
        return self._skillId

    @property
    def criterion(self) -> str:
        return self._criterion

    @property
    def cell(self) -> int:
        return self._cell

    @property
    def transitionMapId(self) -> float:
        return self._transitionMapId

    @property
    def id(self) -> int:
        return self._id

    @property
    def isValid(self) -> bool:
        criterionWhiteList: list = [
            "Ad",
            "DM",
            "MI",
            "Mk",
            "Oc",
            "Pc",
            "QF",
            "Qo",
            "Qs",
            "Sv",
        ]
        if len(self.criterion) != 0:
            if "&" not in self.criterion and "|" not in self.criterion and self.criterion[0:2] in criterionWhiteList:
                return False
            criterion = GroupItemCriterion(self.criterion)
            return criterion.isRespected
        return True

    def __str__(self) -> str:
        res = f"{TransitionTypeEnum(self._type).name}("
        attribs = []
        if self._direction != -1:
            attribs.append(f"direction={DirectionsEnum(self._direction).name}")
        if self._skillId != -1:
            attribs.append(f"skillId={self._skillId}")
        if self._criterion:
            attribs.append(f"criterion={self._criterion} ({self.isValid})")
        if self._transitionMapId:
            attribs.append(f"transitionMapId={self._transitionMapId}")
        if self._cell:
            attribs.append(f"cell={self._cell}")
        if int(self._id) != -1:
            attribs.append(f"id={self._id}")
        res += ", ".join(attribs)
        res += ")"
        return res

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self):
        return {
            "type": self._type,
            "direction": self._direction,
            "skillId": self._skillId,
            "criterion": self._criterion,
            "transitionMapId": self._transitionMapId,
            "cell": self._cell,
            "id": self._id,
        }

    def clone(self):
        return Transition(
            self._type,
            self._direction,
            self._skillId,
            self._criterion,
            self._transitionMapId,
            self._cell,
            self._id,
        )
