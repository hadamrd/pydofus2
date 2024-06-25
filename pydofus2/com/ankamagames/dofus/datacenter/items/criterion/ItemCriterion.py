from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.damageCalculation.tools.StatIds import StatIds

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator


class ItemCriterion(IItemCriterion):

    _serverCriterionForm: str

    _operator: "ItemCriterionOperator"

    _criterionRef: str

    _criterionValue: int

    _criterionValueText: str

    def __init__(self, pCriterion: str):
        super().__init__()
        self._operator = None
        self._criterionRef = ""
        self._criterionValue = 0
        self._criterionValueText = ""
        self._serverCriterionForm = pCriterion
        self.getInfos()

    @property
    def inlineCriteria(self) -> list[IItemCriterion]:
        criteria: list[IItemCriterion] = list[IItemCriterion]()
        criteria.append(self)
        return criteria

    @property
    def criterionValue(self) -> object:
        return self._criterionValue

    @property
    def operatorText(self) -> str:
        return self._operator.text if not self._operator else None

    @property
    def operator(self) -> "ItemCriterionOperator":
        return self._operator

    @property
    def isRespected(self) -> bool:
        player = PlayedCharacterManager()
        if not player or not player.characteristics:
            return True
        return self._operator.compare(self.getCriterion(), float(self._criterionValue))

    @property
    def text(self) -> str:
        return self.buildText(False)

    @property
    def textForTooltip(self) -> str:
        return self.buildText(True)

    @property
    def basicText(self) -> str:
        return self._serverCriterionForm

    def clone(self) -> IItemCriterion:
        return ItemCriterion(self.basicText)

    def buildText(self, forTooltip: bool = False) -> str:
        readableCriterionRef = None

        if self._criterionRef == "CM":
            readableCriterionRef = I18n.getUiText("ui.stats.movementPoints")

        elif self._criterionRef == "CP":
            readableCriterionRef = I18n.getUiText("ui.stats.actionPoints")

        elif self._criterionRef == "CH":
            readableCriterionRef = I18n.getUiText("ui.pvp.honourPoints")

        elif self._criterionRef == "CD":
            readableCriterionRef = I18n.getUiText("ui.pvp.disgracePoints")

        elif self._criterionRef == "CT":
            readableCriterionRef = I18n.getUiText("ui.stats.takleBlock")

        elif self._criterionRef == "Ct":
            readableCriterionRef = I18n.getUiText("ui.stats.takleEvade")

        elif self._criterionRef == "CE":
            readableCriterionRef = I18n.getUiText("ui.common.energyPoints")

        else:
            knownCriteriaList = [
                "CS",
                "Cs",
                "CV",
                "Cv",
                "CA",
                "Ca",
                "CI",
                "Ci",
                "CW",
                "Cw",
                "CC",
                "Cc",
                "PG",
                "PJ",
                "Pj",
                "PM",
                "PA",
                "PN",
                "PE",
                "<NO>",
                "PS",
                "PR",
                "PL",
                "PK",
                "Pg",
                "Pr",
                "Ps",
                "Pa",
                "PP",
                "PZ",
                "CM",
                "Qa",
                "CP",
                "ca",
                "cc",
                "ci",
                "cs",
                "cv",
                "cw",
                "Pl",
            ]
            if self._criterionRef in knownCriteriaList:
                index = knownCriteriaList.index(self._criterionRef)
                readableCriterionRef = I18n.getUiText("ui.item.characteristics").split(",")[index]
            else:
                Logger().warn(f"Unknown criteria '{self._criterionRef}'")
        return f"{readableCriterionRef} {self._operator.text} {self._criterionValue}"

    def getInfos(self) -> None:
        from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import (
            ItemCriterionOperator,
        )

        OPERATORS_LIST = ItemCriterionOperator.OPERATORS_LIST

        for operator in OPERATORS_LIST:
            if self._serverCriterionForm.find(operator) == 2:
                self._operator = ItemCriterionOperator(operator)
                parts = self._serverCriterionForm.split(operator)
                self._criterionRef = parts[0]
                try:
                    self._criterionValue = int(parts[1])
                except ValueError:
                    self._criterionValue = 0
                self._criterionValueText = parts[1]
                break

    def getCriterion(self) -> int:
        criterion: int = 0
        player = PlayedCharacterManager()
        stats = StatsManager().getStats(player.id)

        if stats is None:
            return 0

        elif self._criterionRef == "Ca":
            criterion = stats.getStatBaseValue(StatIds.AGILITY)

        elif self._criterionRef == "CA":
            criterion = stats.getStatTotalValue(StatIds.AGILITY)

        elif self._criterionRef == "Cc":
            criterion = stats.getStatBaseValue(StatIds.CHANCE)

        elif self._criterionRef == "CC":
            criterion = stats.getStatTotalValue(StatIds.CHANCE)

        elif self._criterionRef == "Ce":
            criterion = stats.getStatBaseValue(StatIds.ENERGY_POINTS)

        elif self._criterionRef == "CE":
            criterion = stats.getStatTotalValue(StatIds.MAX_ENERGY_POINTS)

        elif self._criterionRef == "CH":
            criterion = stats.getStatTotalValue(StatIds.HONOUR_POINTS)

        elif self._criterionRef == "Ci":
            criterion = stats.getStatBaseValue(StatIds.INTELLIGENCE)

        elif self._criterionRef == "CI":
            criterion = stats.getStatTotalValue(StatIds.INTELLIGENCE)

        elif self._criterionRef == "CL":
            criterion = stats.getHealthPoints()

        elif self._criterionRef == "CM":
            criterion = stats.getStatTotalValue(StatIds.MOVEMENT_POINTS)

        elif self._criterionRef == "CP":
            criterion = stats.getStatTotalValue(StatIds.ACTION_POINTS)

        elif self._criterionRef == "Cs":
            criterion = stats.getStatBaseValue(StatIds.STRENGTH)

        elif self._criterionRef == "CS":
            criterion = stats.getStatTotalValue(StatIds.STRENGTH)

        elif self._criterionRef == "Cv":
            criterion = stats.getStatBaseValue(StatIds.VITALITY)

        elif self._criterionRef == "CV":
            criterion = stats.getStatTotalValue(StatIds.VITALITY)

        elif self._criterionRef == "Cw":
            criterion = stats.getStatBaseValue(StatIds.WISDOM)

        elif self._criterionRef == "CW":
            criterion = stats.getStatTotalValue(StatIds.WISDOM)

        elif self._criterionRef == "Ct":
            criterion = stats.getStatTotalValue(StatIds.TACKLE_EVADE)

        elif self._criterionRef == "CT":
            criterion = stats.getStatTotalValue(StatIds.TACKLE_BLOCK)

        elif self._criterionRef == "ca":
            criterion = stats.getStatAdditionalValue(StatIds.AGILITY)

        elif self._criterionRef == "cc":
            criterion = stats.getStatAdditionalValue(StatIds.CHANCE)

        elif self._criterionRef == "ci":
            criterion = stats.getStatAdditionalValue(StatIds.INTELLIGENCE)

        elif self._criterionRef == "cs":
            criterion = stats.getStatAdditionalValue(StatIds.STRENGTH)

        elif self._criterionRef == "cv":
            criterion = stats.getStatAdditionalValue(StatIds.VITALITY)

        elif self._criterionRef == "cw":
            criterion = stats.getStatAdditionalValue(StatIds.WISDOM)

        return criterion

    def __repr__(self) -> str:
        return self.text
