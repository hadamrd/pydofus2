from typing import List

from pydofus2.Ankama_Common.Common import Common
from pydofus2.Ankama_Common.ui.items.RecipesFilterWrapper import \
    RecipesFilterWrapper
from pydofus2.Ankama_storage.ui.enum.StorageState import StorageState
from pydofus2.com.ankamagames.berilia.api.UiApi import UiApi
from pydofus2.com.ankamagames.berilia.enums.SelectMethodEnum import \
    SelectMethodEnum
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Recipe import Recipe
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import \
    KnownJobWrapper
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import \
    ProtocolConstantsEnum
from pydofus2.com.ankamagames.dofus.uiApi.JobsApi import JobsApi
from pydofus2.com.ankamagames.dofus.uiApi.PlayedCharacterApi import \
    PlayedCharacterApi
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class Recipes:
    def __init__(self) -> None:
        self.characterApi = PlayedCharacterApi()
        self._recipes = list[Recipe]()
        self._recipeTypes = []
        self._inventoryDataByGID = dict[int, ItemWrapper]()
        self._currentSkillId: int = None
        self._currentJob: KnownJobWrapper = None
        self._canTransfertItems = None
        self._ingredientsToleranceFilter = None
        self._currentRecipesFilter = None
        self._searchCriteria = None
        self._sortCriteria = None
        self._jobsLevel = dict[int, KnownJobWrapper]()
        self._currentRecipe: Recipe = None
        self.chk_showConditionnalRecipes = False
        self.chk_possibleRecipes = True
        self._useJobLevelInsteadOfMaxFilter = False
        self.uiApi = UiApi()

    def load(self, storage, jobId=0, jobLevel=0, skillId=0, ingredientsToleranceFilter=0, uiName="storage"):
        KernelEventsManager().on(KernelEvent.InventoryContent, self.onInventoryUpdate)
        KernelEventsManager().on(KernelEvent.JobLevelUp, self.onJobLevelUp)
        self.uiName = uiName
        self._storageType = storage
        self._canTransfertItems = self._storageType in [StorageState.BANK_UI_MOD, StorageState.BANK_MOD]
        self._lookBankInventory = self._storageType in [
            StorageState.GUILD_CHEST_UI_MOD,
            StorageState.BANK_UI_MOD,
            StorageState.BANK_MOD,
            StorageState.GUILD_CHEST_STORAGE_MOD,
        ]
        Logger().debug(f"LookBankInventory : {self._lookBankInventory}")
        if jobId != 0:
            self._jobsLevel[jobId] = jobLevel
            if jobLevel != JobsApi.getKnownJob(jobId).jobLevel and uiName == "recipesCraft":
                self._useJobLevelInsteadOfMaxFilter = True
        if ingredientsToleranceFilter is not None:
            self._ingredientsToleranceFilter = ingredientsToleranceFilter
        self._inventoryDataByGID = JobsApi.getInventoryData(self._lookBankInventory)
        self.onJobSelected(jobId, skillId, uiName)

    def updateRecipes(self, newSearch=True):
        if newSearch:
            self._recipes = JobsApi.getRecipesByJob(
                self._inventoryDataByGID,
                self._currentSkillId,
                self._currentJob.id if self._currentJob else 0,
                self._canTransfertItems,
                self._ingredientsToleranceFilter,
            )
            Logger().debug(f"Found Recipes by job {self._currentJob} and tolerence filter: {len(self._recipes)}")
            self._recipeTypes = []
            self._recipes = JobsApi.getJobFilteredRecipes(
                self._recipes,
                self._recipeTypes,
                self._currentRecipesFilter.minLevel,
                self._currentRecipesFilter.maxLevel,
                self._searchCriteria,
                self._currentRecipesFilter.typeId,
            )
            Logger().debug(
                f"Found Recipes by lvlmin {self._currentRecipesFilter.minLevel} - lvlmax {self._currentRecipesFilter.maxLevel} + search filter {self._searchCriteria}: {len(self._recipes)}"
            )
            if self._sortCriteria is not None:
                JobsApi.sortRecipesByCriteria(self._recipes, self._sortCriteria, False)
            typeNames = []
            listedTypeIds = []
            i = 1
            typeNames.append({"label": self.uiApi.getText("ui.common.allTypesForObject"), "id": 0})
            self._recipeTypes.sort(key=lambda x: x.name)
            for recipeType in self._recipeTypes:
                if recipeType.id not in listedTypeIds:
                    typeNames.append({"label": recipeType.name, "id": recipeType.id})
                    listedTypeIds.append(recipeType.id)
        visibleRecipes = []
        okRecipes = []
        if self.chk_showConditionnalRecipes:
            visibleRecipes = [r for r in self._recipes if JobsApi.checkCraftVisible(r.resultId) and r.result.visible]
        else:
            visibleRecipes = [
                r
                for r in self._recipes
                if JobsApi.checkCraftVisible(r.resultId)
                and JobsApi.checkCraftConditions(r.resultId)
                and r.result.visible
            ]
        Logger().debug(f"Visible recipes : {len(visibleRecipes)}")
        if self.chk_possibleRecipes:
            for r in visibleRecipes:
                if (
                    (self._currentJob and r.jobId == self._currentJob.id) or not self._currentJob
                ) and r.resultLevel <= self.getJobLevel(r.jobId):
                    recipeOk = True
                    for i in range(len(r.ingredientIds)):
                        if (
                            not self._inventoryDataByGID.get(r.ingredientIds[i])
                            or not self._inventoryDataByGID[r.ingredientIds[i]]["totalQuantity"]
                            or self._inventoryDataByGID[r.ingredientIds[i]]["totalQuantity"] < r.quantities[i]
                        ):
                            recipeOk = False
                            break
                    if recipeOk and JobsApi.checkCraftFeasible(r.resultId):
                        okRecipes.append(r)
            self.fillRecipesGrid(okRecipes)
            Logger().debug(f"Possible recipes : {len(okRecipes)}")
            return okRecipes
        else:
            self.fillRecipesGrid(visibleRecipes)
            return visibleRecipes

    def getJobLevel(self, jobId=0) -> KnownJobWrapper:
        if jobId == 0:
            if not self._currentJob:
                Logger().error("Something's wrong here, no jobId and no currentJob.")
                return 1
            jobId = self._currentJob.id
        if self._jobsLevel.get(jobId, 0) > 0:
            return self._jobsLevel[jobId]
        if self._currentJob:
            return self._currentJob.jobLevel
        self._jobsLevel[jobId] = JobsApi.getKnownJob(jobId).jobLevel
        return self._jobsLevel[jobId]

    def fillRecipesGrid(self, recipes: List) -> None:
        self.gd_recipes = recipes
        # self.sysApi.dispatchHook('CraftHookList.RecipesListRefreshed', len(recipes))

    def getIngredientTotalQuantity(self, itemGID: int) -> int:
        totalQty: int = 0
        if itemGID in self._inventoryDataByGID:
            totalQty = int(self._inventoryDataByGID[itemGID]["totalQuantity"])
        return totalQty

    def itemIsInBag(self, itemGID: int) -> bool:
        itemDetails = self._inventoryDataByGID.get(itemGID, {})
        if not itemDetails or not itemDetails.get("fromBag"):
            return False
        for fromBag in itemDetails["fromBag"]:
            if not fromBag:
                return False
        return True

    def getActualMaxOccurence(self, resultId: int) -> int:
        itemDetails = self._inventoryDataByGID.get(resultId, {})
        maxOccurence = int(itemDetails.get("actualMaxOccurence", 0))
        return maxOccurence

    def getPotentialMaxOccurence(self, resultId: int) -> int:
        itemDetails = self._inventoryDataByGID.get(resultId, {})
        maxOccurence = int(itemDetails.get("potentialMaxOccurence", 0))
        return maxOccurence

    def getPossibleMaxOccurence(self, resultId: int) -> int:
        recipe = JobsApi.getRecipe(resultId)
        occurences = []
        stackTotalQty = 0
        for i in range(len(recipe.ingredientIds)):
            ingredientDetails = self._inventoryDataByGID.get(recipe.ingredientIds[i], {})
            stackTotalQty = 0
            if ingredientDetails and ingredientDetails.get("stackQtyList"):
                for j in range(len(ingredientDetails["stackQtyList"])):
                    if not ingredientDetails["fromBag"][j]:
                        stackTotalQty += ingredientDetails["stackQtyList"][j]
                occurences.append(int(stackTotalQty / recipe.quantities[i]))
            else:
                occurences.append(0)
        occurences.sort()
        maxOccurence = int(occurences[-1]) if occurences else 0
        if maxOccurence == 0:
            maxOccurence = 1
        return maxOccurence

    def calculateIngredientsToRetrieve(self, recipe: Recipe, qty: int = None) -> None:
        """
        The function is responsible for determining the list of ingredientsand their
        quantities needed to craft a certain recipe, taking into account the maximum quantity that the player can carry.
        """
        availablePlayerPods = self.characterApi.inventoryWeightMax() - self.characterApi.inventoryWeight()
        if recipe.resultId not in self._inventoryDataByGID:
            Logger().warning(f"Recipe not possible")
            return [], []
        maxOccurrence = self._inventoryDataByGID[recipe.resultId]["actualMaxOccurence"]
        recipeWeight = sum(
            self._inventoryDataByGID[eid]["weight"] * qty for eid, qty in zip(recipe.ingredientIds, recipe.quantities)
        )
        maxRecepiesCanCarry = availablePlayerPods // recipeWeight
        nbrRecepiesToRetrieve = min(maxOccurrence, maxRecepiesCanCarry)
        if not qty:
            qty = nbrRecepiesToRetrieve
        if qty > nbrRecepiesToRetrieve:
            raise ValueError(f"Player can't carry more than {nbrRecepiesToRetrieve} of the given recipe.")
        ingredients = []
        quantities = []
        required_quantities = []
        l = len(recipe.ingredientIds)
        for i in range(l):
            required_quantities.append(recipe.quantities[i] * qty)
            ingredient_details = self._inventoryDataByGID.get(recipe.ingredientIds[i], None)
            if ingredient_details and ingredient_details["totalQuantity"]:
                found_qty = 0
                ingredient_qty = 0
                ll = len(ingredient_details["stackUidList"])
                for j in range(ll):
                    if not ingredient_details["fromBag"][j]:
                        ingredients.append(ingredient_details["stackUidList"][j])
                        ingredient_qty = ingredient_details["stackQtyList"][j]
                        if not found_qty and ingredient_qty >= required_quantities[i]:
                            quantities.append(required_quantities[i])
                            break
                        if found_qty < required_quantities[i]:
                            if found_qty + ingredient_qty == required_quantities[i]:
                                quantities.append(ingredient_qty)
                                found_qty += ingredient_qty
                                break
                            if found_qty + ingredient_qty > required_quantities[i]:
                                quantities.append(required_quantities[i] - found_qty)
                                found_qty = required_quantities[i]
                                break
                            quantities.append(ingredient_qty)
                            found_qty += ingredient_qty
        return ingredients, quantities

    def onInventoryUpdate(self, event, items, kama):
        self._inventoryDataByGID = {}
        invData = JobsApi.getInventoryData(self._lookBankInventory)
        for index in invData:
            self._inventoryDataByGID[int(index)] = invData[index]
        self.updateRecipes(True)

    def onJobLevelUp(self, event, jobId, jobName, lastJobLevel, newLevel, podsBonus):
        if jobId in self._jobsLevel:
            self._jobsLevel[jobId] = newLevel
        if self._currentJob:
            if self._currentJob.id == jobId:
                self._currentJob = JobsApi.getKnownJob(jobId)
                self._currentRecipesFilter.maxLevel = newLevel
                self.inp_maxLevelSearch = str(self._currentRecipesFilter.maxLevel)
                self.updateRecipes(False)

    def onJobSelected(self, jobId, skillId, uiName):
        if uiName != self.uiName:
            return
        if jobId == 0 and skillId == 0:
            self._currentJob = None
            self._currentSkillId = 0
            self._currentRecipesFilter = RecipesFilterWrapper(0, 1, ProtocolConstantsEnum.MAX_JOB_LEVEL)
        else:
            self._currentJob = JobsApi.getKnownJob(jobId)
            self._currentSkillId = skillId
            self._currentRecipesFilter = Common().getJobSearchOptionsByJobId(self._currentJob.id)
            if self._currentRecipesFilter is None:
                self._currentRecipesFilter = RecipesFilterWrapper(self._currentJob.id, 1, self.getJobLevel())
        self._searchCriteria = None
        self.inp_minLevelSearch = str(self._currentRecipesFilter.minLevel)
        if self._useJobLevelInsteadOfMaxFilter:
            self._currentRecipesFilter.maxLevel = self.getJobLevel()
        self.inp_maxLevelSearch = str(self._currentRecipesFilter.maxLevel)
        self.updateRecipes(True)

    def onSelectItem(self, target, selectMethod, isNewSelection):
        if target == self.gd_recipes:
            if selectMethod != SelectMethodEnum.AUTO and self._currentJob is not None:
                self.gd_recipes["selectedItem"]
                # self.sysApi.dispatchHook(KernelEvent.RecipeSelected, item, self._currentJob.id)
        elif target == self.cb_type:
            if not isNewSelection or self._currentRecipesFilter.typeId == self.cb_type["selectedItem"]["id"]:
                return
            self._currentRecipesFilter.typeId = self.cb_type["selectedItem"]["id"]
            Common().setJobSearchOptionsByJobId(self._currentRecipesFilter)
            self.updateRecipes()

    def applyFilter(self, txtSearch="", minLvl=1, maxLvl=ProtocolConstantsEnum.MAX_JOB_LEVEL):
        if txtSearch != self.uiApi.getText("ui.common.search.input"):
            if len(txtSearch) > 2:
                if self._searchCriteria != txtSearch:
                    self._searchCriteria = txtSearch
                    updateRecipesNeeded = True
            else:
                if self._searchCriteria:
                    self._searchCriteria = None
                if txtSearch == "":
                    updateRecipesNeeded = True
                else:
                    self.fillRecipesGrid([])

        if self._currentRecipesFilter.minLevel != minLvl:
            searchMinLevel = 1
            if not minLvl or minLvl == 0:
                searchMinLevel = 1
            elif minLvl > ProtocolConstantsEnum.MAX_JOB_LEVEL:
                searchMinLevel = ProtocolConstantsEnum.MAX_JOB_LEVEL
            else:
                searchMinLevel = minLvl
            if searchMinLevel > self._currentRecipesFilter.maxLevel:
                searchMinLevel = self._currentRecipesFilter.maxLevel
            self._currentRecipesFilter.minLevel = searchMinLevel
            Common().setJobSearchOptionsByJobId(self._currentRecipesFilter)
            updateRecipesNeeded = True

        if self._currentRecipesFilter.maxLevel != maxLvl:
            searchMaxLevel = 1
            if not maxLvl or maxLvl == 0:
                searchMaxLevel = 1
            elif maxLvl > ProtocolConstantsEnum.MAX_JOB_LEVEL:
                searchMaxLevel = ProtocolConstantsEnum.MAX_JOB_LEVEL
            else:
                searchMaxLevel = maxLvl
            if searchMaxLevel < self._currentRecipesFilter.minLevel:
                searchMaxLevel = self._currentRecipesFilter.minLevel
            self._currentRecipesFilter.maxLevel = searchMaxLevel
            Common().setJobSearchOptionsByJobId(self._currentRecipesFilter)
            updateRecipesNeeded = True

        if updateRecipesNeeded:
            return self.updateRecipes()

        return self.gd_recipes

    def unload(self):
        self._lockSearchTimer = None
        self._inventoryDataByGID = None
        self._recipes = None
        self._currentJob = None
        self._currentRecipe = None
        self._storageType = None
