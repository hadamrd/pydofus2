from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionFactory import ItemCriterionFactory
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class GroupItemCriterion(IItemCriterion):

    _criteria: list[ItemCriterion]
    _operators: list[str]
    _criterionTextForm: str

    def __init__(self, pCriterion: str):
        super().__init__()
        self._criterionTextForm = pCriterion
        self._operators = list[str]()
        self._criteria = list[ItemCriterion]()
        self.parse()

    @classmethod
    def create(cls, pCriteria: list[ItemCriterion], pOperators: list[str]) -> "GroupItemCriterion":
        textForm = ""
        criterionIndex = 0
        operatorIndex = 0
        tabLength = len(pCriteria) + len(pOperators)

        for i in range(tabLength):
            if i % 2 == 0:
                textForm += pCriteria[criterionIndex].basicText
                criterionIndex += 1
            else:
                textForm += pOperators[operatorIndex]
                operatorIndex += 1

        return GroupItemCriterion(textForm)

    @property
    def criteria(self) -> list[ItemCriterion]:
        return self._criteria

    @property
    def inlineCriteria(self) -> list[ItemCriterion]:
        criteria = list[ItemCriterion]()
        for criterion in self._criteria:
            criteria = criteria.extend(criterion.inlineCriteria)
        return criteria

    @property
    def isRespected(self) -> bool:
        if not self._criteria:
            return True

        player = PlayedCharacterManager()

        if not player or not player.characteristics:
            Logger().error("Character or characteristics doesn't exist !, returning true")
            return True

        if self._criteria and len(self._criteria) == 1 and isinstance(self._criteria[0], IItemCriterion):
            return self._criteria[0].isRespected

        if len(self._operators) > 0 and self._operators[0] == "|":
            for criterion in self._criteria:
                if criterion.isRespected:
                    return True
            return False

        for criterion in self._criteria:
            if criterion is None:
                raise ValueError(f"One of the criterion is null, full criteria: {self._criterionTextForm}")
            if not criterion.isRespected:
                return False

        return True

    @property
    def text(self) -> str:
        textForm = ""
        if not self._criteria:
            return textForm
        tabLength = len(self._criteria) + len(self._operators)
        criterionIndex = 0
        operatorIndex = 0
        for i in range(tabLength):
            if textForm:
                textForm += " "
            if i % 2 == 0:
                textForm += self._criteria[criterionIndex].text
                criterionIndex += 1
            else:
                textForm += self._operators[operatorIndex]
                operatorIndex += 1
        return textForm

    @property
    def basicText(self) -> str:
        return self._criterionTextForm

    def clone(self) -> IItemCriterion:
        return GroupItemCriterion(self.basicText)

    def parse(self):
        position = 0
        stack = []
        while position < len(self._criterionTextForm):
            char = self._criterionTextForm[position]

            if char == "(":
                stack.append(position)
                position += 1

            elif char == ")":
                if not stack:
                    raise ValueError(f"Unmatched parenthesis at position {position}")

                start_pos = stack.pop()
                if not stack:
                    group_content = self._criterionTextForm[start_pos + 1 : position]
                    nested_group = GroupItemCriterion(group_content)
                    self._criteria.append(nested_group)
                position += 1

            elif char in ["&", "|"] and not stack:
                self._operators.append(char)
                position += 1

            else:
                if not stack:
                    criterion_end = self.find_next_operator_or_parenthesis(position)
                    criterion = self._criterionTextForm[position:criterion_end].strip()
                    criteria = ItemCriterionFactory.create(criterion)
                    if criteria is not None:
                        self._criteria.append(criteria)
                    position = criterion_end
                else:
                    position += 1

        if stack:
            raise ValueError(f"Unmatched parenthesis at position {stack.pop()}")

        if len(self._criteria) == 1 and isinstance(self._criteria[0], GroupItemCriterion):
            top_group = self._criteria[0]
            self._criteria = top_group._criteria
            self._operators = top_group._operators

    def find_next_operator_or_parenthesis(self, start_pos):
        for pos in range(start_pos, len(self._criterionTextForm)):
            if self._criterionTextForm[pos] in ["&", "|", "(", ")"]:
                return pos
        return len(self._criterionTextForm)

    @property
    def operators(self) -> list[str]:
        return self._operators

    def __repr__(self):
        return self.text


if __name__ == "__main__":
    # cr = GroupItemCriterion('((Qo>3613&PO<11044,1&Qo<3597)')
    cr = GroupItemCriterion("(Qo>3613&PO<11044,1&Qo<3597)")
    print(cr.text)
    print(cr.operators)
    print("number of criterias ", len(cr.criteria))
