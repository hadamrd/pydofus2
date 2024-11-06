import unicodedata
from typing import List

from pydofus2.com.ankamagames.berilia.interfaces.IApi import IApi
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Recipe import Recipe
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import KnownJobWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobDescription import JobDescription
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class JobsApi(IApi):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def getRecipe(cls, objectId: int) -> Recipe:
        return Recipe.getRecipeByResultId(objectId)

    @classmethod
    def getRecipesByJob(
        cls, details, skillId=0, jobId=0, fromBank=False, missingIngredientsTolerance=8
    ) -> List[Recipe]:
        allRecipes = []
        recipes = []
        if skillId > 0:
            allRecipes = Recipe.getAllRecipesForSkillId(skillId, ProtocolConstantsEnum.MAX_JOB_LEVEL)
        elif jobId > 0:
            allRecipes = Recipe.getRecipesByJobId(jobId)
        else:
            allRecipes = Recipe.getAllRecipes()
        for recipe in allRecipes:
            if (recipe.job and jobId != 0) or recipe.jobId != DataEnum.JOB_ID_BASE:
                requiredQty = sum(recipe.quantities)
                totalQty = 0
                foundIngredients = 0
                foundIngredientsQty = 0
                occurrences = []
                missingIngredients = missingIngredientsTolerance
                for ingredientId, ingredientQty in zip(recipe.ingredientIds, recipe.quantities):
                    totalQty = int(details.get(ingredientId, {"totalQuantity": 0}).get("totalQuantity", 0))
                    if totalQty >= ingredientQty:
                        occurrences.append(int(totalQty // ingredientQty))
                        foundIngredientsQty += ingredientQty
                        foundIngredients += 1
                    else:
                        occurrences.append(0)
                        missingIngredients -= 1
                    if missingIngredients < 0:
                        break
                if missingIngredients < 0:
                    continue
                if (
                    (foundIngredients == len(recipe.ingredientIds) and foundIngredientsQty >= requiredQty)
                    or (missingIngredientsTolerance == 8)
                    or (
                        missingIngredientsTolerance > 0
                        and foundIngredients + missingIngredientsTolerance >= len(recipe.ingredientIds)
                    )
                ):
                    recipes.append(recipe)
                    occurrences.sort()
                    if recipe.resultId not in details:
                        details[recipe.resultId] = {"actualMaxOccurence": occurrences[0]}
                    else:
                        details[recipe.resultId]["actualMaxOccurence"] = occurrences[0]
                    if fromBank:
                        potentialMaxOccurrence = 0
                        for val in occurrences:
                            if val != 0:
                                potentialMaxOccurrence = val
                                break
                        details[recipe.resultId]["potentialMaxOccurence"] = potentialMaxOccurrence
        return recipes

    @staticmethod
    def getJobFilteredRecipes(
        recipes: List["Recipe"],
        resultTypes: List,
        minLevel: int = 1,
        maxLevel: int = 1,
        search: str = None,
        typeId: int = 0,
    ) -> List["Recipe"]:
        okForLevel = False
        okForType = False
        okForSearch = False
        recipesResult = []
        if search:
            search = "".join(
                c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"
            ).lower()
        for recipe in recipes:
            if recipe:
                okForLevel = False
                okForType = False
                okForSearch = False
                if minLevel > 1 or maxLevel < ProtocolConstantsEnum.MAX_JOB_LEVEL:
                    if minLevel <= recipe.resultLevel <= maxLevel:
                        okForLevel = True
                    else:
                        okForLevel = False
                else:
                    okForLevel = True
                if typeId > 0:
                    if recipe.resultTypeId == typeId:
                        okForType = True
                    else:
                        okForType = False
                else:
                    okForType = True
                if okForLevel and okForType and search:
                    if search in recipe.words:
                        okForSearch = True
                    else:
                        okForSearch = False
                else:
                    okForSearch = True
                if okForLevel and okForSearch:
                    if recipe.result.type not in resultTypes:
                        resultTypes.append(recipe.result.type)
                    if okForType:
                        recipesResult.append(recipe)
        return recipesResult

    @classmethod
    def sortRecipesByCriteria(cls, recipes, sortCriteria, sortDescending):
        cls.sortRecipes(recipes, sortCriteria, 1 if sortDescending else -1)
        return recipes

    @classmethod
    def sortRecipes(cls, recipes: list[Recipe], criteria, way=1):
        if criteria == "level":
            recipes.sort(key=cls.compareLevel(way))
        elif criteria == "price":
            recipes.sort(key=cls.comparePrice(way))

    @classmethod
    def compareLevel(cls, way=1):
        def comparison(a: Recipe, b: Recipe):
            if a.resultLevel < b.resultLevel:
                return -way
            if a.resultLevel > b.resultLevel:
                return way
            return a.resultName < b.resultName

        return comparison

    @classmethod
    def comparePrice(cls, way=1):
        def comparison(a: Recipe, b: Recipe):
            aL = Kernel().averagePricesFrame.pricesData.items[a.resultId]
            bL = Kernel().averagePricesFrame.pricesData.items[b.resultId]
            if not aL:
                aL = ProtocolConstantsEnum.MAX_KAMA if way == 1 else 0
            if not bL:
                bL = ProtocolConstantsEnum.MAX_KAMA if way == 1 else 0
            if aL < bL:
                return -way
            if aL > bL:
                return way
            return a.resultName < b.resultName

        return comparison

    @classmethod
    def getJobDescription(cls, jobId):
        kj = cls.getKnownJob(jobId)
        if not kj:
            return None
        return kj.jobDescription

    @classmethod
    def getSkillActionDescription(cls, jd: JobDescription, skillId):
        for sd in jd.skills:
            if sd.skillId == skillId:
                return sd
        return None

    @classmethod
    def getKnownJobs(cls):
        knownJobs = [kj for kj in PlayedCharacterManager().jobs.values() if kj is not None]
        return knownJobs

    @classmethod
    def getKnownJob(cls, jobId):
        if not PlayedCharacterManager().jobs:
            return None
        if jobId == "JOB_ID_BASE":
            kj = KnownJobWrapper(1, "MAX_JOB_LEVEL")
        else:
            kj = PlayedCharacterManager().jobs.get(jobId)
        return kj

    @classmethod
    def checkCraftConditions(cls, objectId: int) -> bool:
        it = Item.getItemById(objectId)
        gic = it.craftConditions if it else None
        return gic.isRespected if gic else True

    @classmethod
    def checkCraftVisible(cls, objectId: int) -> bool:
        it = Item.getItemById(objectId)
        gic = it.craftVisibleConditions if it else None
        return gic.isRespected if gic else True

    @classmethod
    def checkCraftFeasible(cls, objectId: int) -> bool:
        it = Item.getItemById(objectId)
        gic = it.craftFeasibleConditions if it else None
        return gic.isRespected if gic else True

    @classmethod
    def getRecipesList(cls, objectId: int) -> list:
        recipeList = Item.getItemById(objectId).recipes
        return recipeList if recipeList else []

    @classmethod
    def getJobName(cls, pJobId: int) -> str:
        job = Job.getJobById(pJobId)
        if job:
            return job.name
        Logger().error(f"We want the name of a non-existing job (id : {pJobId})")
        return ""

    @classmethod
    def getInventoryData(cls, fromBank=False):
        details = {}
        if fromBank:
            resourceItems = InventoryManager().bankInventory.getView("bank").content
        else:
            resourceItems = InventoryManager().inventory.getView("storage").content
        for ingredient in resourceItems:
            if not ingredient.linked:
                if ingredient.objectGID not in details:
                    details[ingredient.objectGID] = {
                        "totalQuantity": ingredient.quantity,
                        "stackUidList": [ingredient.objectUID],
                        "stackQtyList": [ingredient.quantity],
                        "fromBag": [False],
                        "storageTotalQuantity": ingredient.quantity,
                        "weight": ingredient.weight,
                    }
                else:
                    details[ingredient.objectGID]["totalQuantity"] += ingredient.quantity
                    details[ingredient.objectGID]["stackUidList"].append(ingredient.objectUID)
                    details[ingredient.objectGID]["stackQtyList"].append(ingredient.quantity)
                    details[ingredient.objectGID]["fromBag"].append(False)
                    details[ingredient.objectGID]["storageTotalQuantity"] += ingredient.quantity
        if fromBank:
            bagItems = InventoryManager().inventory.getView("storage").content
            for ingredient in bagItems:
                if not ingredient.linked:
                    if ingredient.objectGID not in details:
                        details[ingredient.objectGID] = {
                            "totalQuantity": ingredient.quantity,
                            "stackUidList": [ingredient.objectUID],
                            "stackQtyList": [ingredient.quantity],
                            "fromBag": [True],
                            "weight": ingredient.weight,
                        }
                    else:
                        details[ingredient.objectGID]["totalQuantity"] += ingredient.quantity
                        details[ingredient.objectGID]["stackUidList"].append(ingredient.objectUID)
                        details[ingredient.objectGID]["stackQtyList"].append(ingredient.quantity)
                        details[ingredient.objectGID]["fromBag"].append(True)
        return details
