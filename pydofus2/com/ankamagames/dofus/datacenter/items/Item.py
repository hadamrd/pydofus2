import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance

from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import \
    GroupItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemSet import ItemSet
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemType import ItemType
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.types.enums.ItemCategoryEnum import \
    ItemCategoryEnum
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.data.IPostInit import IPostInit
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.jobs.Recipe import Recipe


class Item(IPostInit, IDataCenter):

    MODULE: str = "Items"

    SUPERTYPE_NOT_EQUIPABLE: list = [
        DataEnum.ITEM_SUPERTYPE_RESOURCES,
        DataEnum.ITEM_SUPERTYPE_QUEST_ITEMS,
        DataEnum.ITEM_SUPERTYPE_MUTATIONS,
        DataEnum.ITEM_SUPERTYPE_FOODS,
        DataEnum.ITEM_SUPERTYPE_BLESSINGS,
        DataEnum.ITEM_SUPERTYPE_CURSES,
        DataEnum.ITEM_SUPERTYPE_CONSUMABLE,
        DataEnum.ITEM_SUPERTYPE_ROLEPLAY_BUFFS,
        DataEnum.ITEM_SUPERTYPE_FOLLOWERS,
        DataEnum.ITEM_SUPERTYPE_MOUNTS,
        DataEnum.ITEM_SUPERTYPE_CATCHING_ITEMS,
        DataEnum.ITEM_SUPERTYPE_LIVING_ITEMS,
    ]

    MAX_JOB_LEVEL_GAP: int = 100

    _censoredIcons: dict

    id: int

    nameId: int

    typeId: int

    descriptionId: int

    iconId: int

    level: int

    realWeight: int = None

    cursed: bool

    useAnimationId: int

    usable: bool

    targetable: bool

    exchangeable: bool

    price: float

    twoHanded: bool

    etheral: bool

    itemSetId: int

    criteria: str

    criteriaTarget: str

    hideEffects: bool

    enhanceable: bool

    nonUsableOnAnother: bool

    appearanceId: int

    secretRecipe: bool

    dropMonsterIds: list[int]

    dropTemporisMonsterIds: list[int]

    recipeSlots: int

    recipeIds: list[int]

    objectIsDisplayOnWeb: bool

    bonusIsSecret: bool

    possibleEffects: list["EffectInstance"]

    evolutiveEffectIds: list[int]

    favoriteSubAreas: list[int]

    favoriteSubAreasBonus: int

    craftXpRatio: int

    craftVisible: str

    craftConditional: str

    craftFeasible: str

    needUseConfirm: bool

    isDestructible: bool

    isLegendary: bool

    isSaleable: bool

    nuggetsBySubarea: list[list[float]]

    containerIds: list[int]

    resourcesBySubarea: list[list[int]]

    visibility: str

    importantNoticeId: int

    changeVersion: str

    tooltipExpirationDate: float = None

    _name: str = None

    _undiatricalName: str

    _description: str

    _type: ItemType = None

    _weight: int = None

    _itemSet: ItemSet = None

    _conditions: GroupItemCriterion = None

    _conditionsTarget: GroupItemCriterion = None

    _craftVisibleConditions: GroupItemCriterion = None

    _craftConditions: GroupItemCriterion = None

    _craftFeasibleConditions: GroupItemCriterion = None

    _recipes: list = None

    _craftXpByJobLevel: dict

    _nuggetsQuantity: float = 0

    _basicExperienceAsFood: float = 0

    _importantNotice: str = None

    _processedImportantNotice: str = None

    def __init__(self):
        super().__init__()
        self.id: int = None

        self.nameId: int = None

        self.typeId: int = None

        self.descriptionId: int = None

        self.iconId: int = None

        self.level: int = None

        self.realWeight: int

        self.cursed: bool = None

        self.useAnimationId: int = None

        self.usable: bool = None

        self.targetable: bool = None

        self.exchangeable: bool = None

        self.price: float = None

        self.twoHanded: bool = None

        self.etheral: bool = None

        self.itemSetId: int = None

        self.criteria: str = None

        self.criteriaTarget: str = None

        self.hideEffects: bool = None

        self.enhanceable: bool = None

        self.nonUsableOnAnother: bool = None

        self.appearanceId: int = None

        self.secretRecipe: bool = None

        self.dropMonsterIds: list[int] = None

        self.dropTemporisMonsterIds: list[int] = None

        self.recipeSlots: int = None

        self.recipeIds: list[int] = None

        self.objectIsDisplayOnWeb: bool = None

        self.bonusIsSecret: bool = None

        self.possibleEffects: list["EffectInstance"] = None

        self.evolutiveEffectIds: list[int] = None

        self.favoriteSubAreas: list[int] = None

        self.favoriteSubAreasBonus: int = None

        self.craftXpRatio: int = None

        self.craftVisible: str = None

        self.craftConditional: str = None

        self.craftFeasible: str = None

        self.needUseConfirm: bool = None

        self.isDestructible: bool = None

        self.isLegendary: bool = None

        self.isSaleable: bool = None

        self.nuggetsBySubarea: list[list[float]] = None

        self.containerIds: list[int] = None

        self.resourcesBySubarea: list[list[int]] = None

        self.visibility: str = None

        self.importantNoticeId: int = None

        self.changeVersion: str = None

        self.tooltipExpirationDate: float = None

        self._description = None

    @classmethod
    def getItemById(cls, id: int, returnDefaultItemIfNull: bool = True) -> "Item":
        if type(id) is not int:
            raise TypeError(f"id must be an int got '{type(id).__name__}' of value '{id}' instead")
        item: Item = GameData().getObject(cls.MODULE, id)
        if item or not returnDefaultItemIfNull:
            return item
        Logger().error(f"Impossible de trouver l'objet {id}, remplacement par l'objet 666")
        return GameData().getObject(cls.MODULE, 666)

    @classmethod
    def getItems(cls) -> list["Item"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getItemById, getItems)

    def getItemsByIds(cls, ids: list[int]) -> list["Item"]:
        id = None
        item = None
        items: list[Item] = list[Item]()
        for id in ids:
            item = GameData().getObject(cls.MODULE, id)
            if item:
                items.append(item)
        return items

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int) -> None:
        self._weight = value

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def undiatricalName(self) -> str:
        if not self._undiatricalName:
            self._undiatricalName = I18n.getUnDiacriticalText(self.nameId)
        return self._undiatricalName

    @property
    def description(self) -> str:
        if not self._description:
            if self.etheral:
                self._description = I18n.getUiText("ui.common.etherealWeaponDescription")
            else:
                self._description = I18n.getText(self.descriptionId)
        return self._description

    @property
    def importantNotice(self) -> str:
        if not self._importantNotice:
            self._importantNotice = I18n.getText(self.importantNoticeId)
        return self._importantNotice

    @property
    def processedImportantNotice(self) -> str:
        if self._processedImportantNotice is not None:
            return self._processedImportantNotice
        if not self.importantNotice:
            return None
        self._processedImportantNotice = HyperlinkMapPosition.parseMapLinks(self.importantNotice)
        return self._processedImportantNotice

    @property
    def type(self) -> "ItemType":
        if not self._type:
            self._type = ItemType.getItemTypeById(self.typeId)
        return self._type

    @property
    def isWeapon(self) -> bool:
        return False

    @property
    def itemSet(self) -> ItemSet:
        if not self._itemSet:
            self._itemSet = ItemSet.getItemSetById(self.itemSetId)
        return self._itemSet

    @property
    def recipes(self) -> list["Recipe"]:
        from pydofus2.com.ankamagames.dofus.datacenter.jobs.Recipe import \
            Recipe

        if not self._recipes:
            numRecipes = len(self.recipeIds)
            self._recipes = list()
            for i in range(numRecipes):
                recipe = Recipe.getRecipeByResultId(self.recipeIds[i])
                if recipe:
                    it = Item.getItemById(recipe.resultId)
                    gic = it.craftVisibleConditions if it else None
                    if not gic or gic.isRespected:
                        self._recipes.append(recipe)
        return self._recipes

    @property
    def category(self) -> int:
        if self.typeId == 0 or not self.type:
            return ItemCategoryEnum.OTHER_CATEGORY
        return self.type.categoryId

    @property
    def conditions(self) -> GroupItemCriterion:
        if not self.criteria:
            return None
        if not self._conditions:
            self._conditions = GroupItemCriterion(self.criteria)
        return self._conditions

    @property
    def targetConditions(self) -> GroupItemCriterion:
        if not self.criteriaTarget:
            return None
        if not self._conditionsTarget:
            self._conditionsTarget = GroupItemCriterion(self.criteriaTarget)
        return self._conditionsTarget

    @property
    def craftVisibleConditions(self) -> GroupItemCriterion:
        if not self.craftVisible:
            return None
        if not self._craftVisibleConditions:
            self._craftVisibleConditions = GroupItemCriterion(self.craftVisible)
        return self._craftVisibleConditions

    @property
    def craftConditions(self) -> GroupItemCriterion:
        if not self.craftConditional:
            return None
        if not self._craftConditions:
            self._craftConditions = GroupItemCriterion(self.craftConditional)
        return self._craftConditions

    @property
    def craftFeasibleConditions(self) -> GroupItemCriterion:
        if not self.craftFeasible:
            return None
        if not self._craftFeasibleConditions:
            self._craftFeasibleConditions = GroupItemCriterion(self.craftFeasible)
        return self._craftFeasibleConditions

    def getCraftXpByJobLevel(self, jobLevel: int) -> int:
        xpWithRatio: float = None
        basicXp: float = None
        if not self._craftXpByJobLevel:
            self._craftXpByJobLevel = dict()
        if not self._craftXpByJobLevel[jobLevel]:
            if jobLevel - self.MAX_JOB_LEVEL_GAP > self.level:
                self._craftXpByJobLevel[jobLevel] = 0
                return self._craftXpByJobLevel[jobLevel]
            basicXp = 20 * self.level / (math.pow(jobLevel - self.level, 1.1) / 10 + 1)
            if self.craftXpRatio > -1:
                xpWithRatio = basicXp * (self.craftXpRatio / 100)
            elif self.type.craftXpRatio > -1:
                xpWithRatio = basicXp * (self.type.craftXpRatio / 100)
            else:
                xpWithRatio = basicXp
            self._craftXpByJobLevel[jobLevel] = math.floor(xpWithRatio)
        return self._craftXpByJobLevel[jobLevel]

    @property
    def nuggetsQuantity(self) -> float:
        nuggets: list[float] = None
        if self._nuggetsQuantity == 0:
            for nuggets in self.nuggetsBySubarea:
                self._nuggetsQuantity += nuggets[1]
        return self._nuggetsQuantity

    @property
    def basicExperienceAsFood(self) -> float:
        experienceInt: int = 0
        if self._basicExperienceAsFood == 0:
            self._basicExperienceAsFood = self.nuggetsQuantity / len(self.nuggetsBySubarea)
            experienceInt = math.floor(self._basicExperienceAsFood * 100000)
            self._basicExperienceAsFood = experienceInt / 100000
        return self._basicExperienceAsFood

    @classmethod
    def copy(cls, src: "Item", to: "Item") -> None:
        to.id = src.id
        to.nameId = src.nameId
        to.typeId = src.typeId
        to.descriptionId = src.descriptionId
        to.iconId = src.iconId
        to.level = src.level
        to.cursed = src.cursed
        to.useAnimationId = src.useAnimationId
        to.usable = src.usable
        to.targetable = src.targetable
        to.price = src.price
        to.twoHanded = src.twoHanded
        to.etheral = src.etheral
        to.enhanceable = src.enhanceable
        to.nonUsableOnAnother = src.nonUsableOnAnother
        to.itemSetId = src.itemSetId
        to.criteria = src.criteria
        to.criteriaTarget = src.criteriaTarget
        to.hideEffects = src.hideEffects
        to.appearanceId = src.appearanceId
        to.recipeIds = src.recipeIds
        to.recipeSlots = src.recipeSlots
        to.secretRecipe = src.secretRecipe
        to.bonusIsSecret = src.bonusIsSecret
        to.objectIsDisplayOnWeb = src.objectIsDisplayOnWeb
        to.possibleEffects = src.possibleEffects
        to.evolutiveEffectIds = src.evolutiveEffectIds
        to.favoriteSubAreas = src.favoriteSubAreas
        to.favoriteSubAreasBonus = src.favoriteSubAreasBonus
        to.dropMonsterIds = src.dropMonsterIds
        to.dropTemporisMonsterIds = src.dropTemporisMonsterIds
        to.resourcesBySubarea = src.resourcesBySubarea
        to.exchangeable = src.exchangeable
        to.craftXpRatio = src.craftXpRatio
        to.needUseConfirm = src.needUseConfirm
        to.isDestructible = src.isDestructible
        to.isLegendary = src.isLegendary
        to.isSaleable = src.isSaleable
        to.craftVisible = src.craftVisible
        to.craftConditional = src.craftConditional
        to.craftFeasible = src.craftFeasible
        to.nuggetsBySubarea = src.nuggetsBySubarea
        to.containerIds = src.containerIds
        to.visibility = src.visibility
        to.importantNoticeId = src.importantNoticeId
        to.changeVersion = src.changeVersion
        to.tooltipExpirationDate = src.tooltipExpirationDate
        to.weight = src.weight
        to.realWeight = src.realWeight

    def postInit(self) -> None:
        pass

    def isEvolutive(self) -> bool:
        return self.evolutiveEffectIds and len(self.evolutiveEffectIds) > 0

    @property
    def visible(self) -> bool:

        if not self.visibility:
            return True
        gic = GroupItemCriterion(self.visibility)
        return gic.isRespected
