from pydofus2.com.ankamagames.dofus.datacenter.breeds.Breed import Breed
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.FeatureManager import (
    FeatureManager,
)
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.dofus.datacenter.optionalFeatures.CustomModeBreedSpell import (
    CustomModeBreedSpell,
)
from pydofus2.com.ankamagames.dofus.datacenter.spells.FinishMove import FinishMove
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellVariant import SpellVariant
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import (
    SpellModifiersManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import (
    SpellManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.actions.FinishMoveListRequestAction import (
    FinishMoveListRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.actions.FinishMoveSetRequestAction import (
    FinishMoveSetRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.actions.SpellVariantActivationRequestAction import (
    SpellVariantActivationRequestAction,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.SlaveSwitchContextMessage import (
    SlaveSwitchContextMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.spell.SpellVariantActivationMessage import (
    SpellVariantActivationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.spell.SpellVariantActivationRequestMessage import (
    SpellVariantActivationRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.finishmoves.FinishMoveListMessage import (
    FinishMoveListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.finishmoves.FinishMoveListRequestMessage import (
    FinishMoveListRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.finishmoves.FinishMoveSetRequestMessage import (
    FinishMoveSetRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.spells.SpellListMessage import (
    SpellListMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightSpellCooldown import (
    GameFightSpellCooldown,
)

from pydofus2.com.ankamagames.dofus.uiApi.PlayedCharacterApi import PlayedCharacterApi
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from functools import cmp_to_key

logger = Logger("Dofus2")


class SpellInventoryManagementFrame(Frame, metaclass=Singleton):

    _spellsGlobalCooldowns: dict[int, list[GameFightSpellCooldown]]()

    def __init__(self):
        self._fullSpellList = dict[int, list[SpellWrapper]]()
        self._spellsGlobalCooldowns = dict()
        super().__init__()

    def getCurrentInstance(self) -> "SpellInventoryManagementFrame":
        return Kernel().worker.getFrame("SpellInventoryManagementFrame")

    def generateCurrentCustomModeBreedSpells(self) -> list:
        spellId: int = 0
        customSpells: list = []
        playerBreed: int = PlayedCharacterApi.getPlayedCharacterInfo().breed
        spellsInventory: list[SpellWrapper] = PlayedCharacterApi.getSpellInventory()
        allSpellIds: list = PlayedCharacterApi.getCustomModeSpellIds()
        customModeBreedSpell: CustomModeBreedSpell = None
        for spellWrapper in spellsInventory:
            spellId = spellWrapper.spell.id
            if spellId in allSpellIds:
                customModeBreedSpell = PlayedCharacterApi.getCustomModeBreedSpellById(spellId)
                if not (customModeBreedSpell == None or customModeBreedSpell.breedId is not playerBreed):
                    customSpells.append([spellWrapper])
        return customSpells

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:
        if isinstance(msg, SpellListMessage):
            slmsg = msg
            alternativeBreedSpells = FeatureManager().isFeatureWithKeywordEnabled("character.spell.breed.alternative")
            playerId = PlayedCharacterManager().id
            self._fullSpellList[playerId] = list()
            idsList = list()
            for spell in slmsg.spells:
                spellData = Spell.getSpellById(spell.spellId)
                if spellData == None:
                    logger.warn("Unknown spell with id " + spell.spellId)
                elif not spellData.spellVariant:
                    self._fullSpellList[playerId].append(
                        SpellWrapper.create(
                            spell.spellId,
                            spell.spellLevel,
                            True,
                            PlayedCharacterManager().id,
                            True,
                        )
                    )
                    if alternativeBreedSpells:
                        idsList.append(spell.spellId)
                else:
                    for spellInVariantData in spellData.spellVariant.spells:
                        if spellInVariantData.id == spell.spellId:
                            self._fullSpellList[playerId].append(
                                SpellWrapper.create(
                                    spellInVariantData.id,
                                    spell.spellLevel,
                                    True,
                                    PlayedCharacterManager().id,
                                    True,
                                )
                            )
                        else:
                            self._fullSpellList[playerId].append(
                                SpellWrapper.create(
                                    spellInVariantData.id,
                                    0,
                                    True,
                                    PlayedCharacterManager().id,
                                )
                            )
                        idsList.append(spellInVariantData.id)
            if slmsg.spellPrevisualization:
                if alternativeBreedSpells:
                    customModeBreedSpells = CustomModeBreedSpell.getCustomModeBreedSpellList(
                        PlayedCharacterManager().infos.breed
                    )
                    for index in range(len(customModeBreedSpells)):
                        spellId = customModeBreedSpells[index].id
                        if spellId in idsList:
                            spellData = Spell.getSpellById(spellId)
                            if spellData == None:
                                logger.warn("Unknown spell with id " + spellId)
                            elif not spellData.spellVariant:
                                self._fullSpellList[playerId].append(
                                    SpellWrapper.create(
                                        spellData.id,
                                        0,
                                        True,
                                        PlayedCharacterManager().id,
                                        True,
                                    )
                                )
                            else:
                                for spellInVariantData in spellData.spellVariant.spells:
                                    if spellInVariantData.id == spellData.id:
                                        self._fullSpellList[playerId].append(
                                            SpellWrapper.create(
                                                spellInVariantData.id,
                                                0,
                                                True,
                                                PlayedCharacterManager().id,
                                                True,
                                            )
                                        )
                                    else:
                                        self._fullSpellList[playerId].append(
                                            SpellWrapper.create(
                                                spellInVariantData.id,
                                                0,
                                                True,
                                                PlayedCharacterManager().id,
                                            )
                                        )
                else:
                    playerBreed = Breed.getBreedById(PlayedCharacterManager().infos.breed)
                    for spellVariant in playerBreed.breedSpellVariants:
                        for swBreed in spellVariant.spells:
                            if swBreed.id not in idsList:
                                self._fullSpellList[playerId].append(
                                    SpellWrapper.create(swBreed.id, 0, True, PlayedCharacterManager().id)
                                )
            PlayedCharacterManager().spellsInventory = self._fullSpellList[playerId]
            PlayedCharacterManager().playerSpellList = self._fullSpellList[playerId]
            return True

        elif isinstance(msg, SlaveSwitchContextMessage):
            sscmsg = msg
            slaveId = sscmsg.slaveId
            spellCastManager = CurrentPlayedFighterManager().getSpellCastManagerById(slaveId)
            spellCastManager.currentTurn = sscmsg.slaveTurn
            self._fullSpellList[slaveId] = []
            for spellInvoc in sscmsg.slaveSpells:
                spellWrapper: SpellWrapper = SpellWrapper.getSpellWrapperById(spellInvoc.spellId, slaveId)
                if (
                    spellWrapper == None
                    or spellWrapper.spellLevel is not spellInvoc.spellLevel
                    or spellWrapper.playerId != slaveId
                ):
                    spellWrapper = SpellWrapper.create(spellInvoc.spellId, spellInvoc.spellLevel, True, slaveId)
                self._fullSpellList[slaveId].append(spellWrapper)
            PlayedCharacterManager().spellsInventory = self._fullSpellList[slaveId]
            CurrentPlayedFighterManager().setCharacteristicsInformations(slaveId, sscmsg.slaveStats)
            StatsManager().addRawStats(slaveId, sscmsg.slaveStats.characteristics)
            SpellModifiersManager().setRawSpellsModifiers(slaveId, sscmsg.slaveStats.spellModifications)
            if CurrentPlayedFighterManager().getSpellCastManagerById(slaveId).needCooldownUpdate:
                CurrentPlayedFighterManager().getSpellCastManagerById(slaveId).updateCooldowns()
            sgcds = self._spellsGlobalCooldowns.get(slaveId)
            if sgcds:
                for gfsc in sgcds:
                    gcdvalue = gfsc.cooldown
                    spellKnown = False
                    for sw in self._fullSpellList[slaveId]:
                        if sw.spellId == gfsc.spellId:
                            spellKnown = True
                            spellLevel = sw.spellLevel
                            if gcdvalue == -1:
                                gcdvalue = sw.spellLevelInfos.minCastInterval
                    if spellKnown:
                        if not spellCastManager.getSpellManagerBySpellId(gfsc.spellId):
                            spellCastManager.castSpell(gfsc.spellId, spellLevel, [], False)
                            spellManager = spellCastManager.getSpellManagerBySpellId(gfsc.spellId)
                            spellManager.forceCooldown(gcdvalue)
                        else:
                            spellManager = spellCastManager.getSpellManagerBySpellId(gfsc.spellId)
                            if spellManager.cooldown <= gcdvalue:
                                spellManager.forceCooldown(gcdvalue)
                sgcds.clear()
                del self._spellsGlobalCooldowns[slaveId]
            playerManager = PlayedCharacterManager()
            spellLevelInfo = None
            for spellWrapper in playerManager.spellsInventory:
                spellLevelInfo = spellWrapper.spellLevelInfos
                if spellLevelInfo.initialCooldown > 0:
                    if spellLevelInfo.initialCooldown > spellCastManager.currentTurn:
                        spellManager = spellCastManager.getSpellManagerBySpellId(spellWrapper.id)
                        if spellManager == None:
                            spellManager = spellCastManager.getSpellManagerBySpellId(
                                spellWrapper.id, True, spellWrapper.spellLevel
                            )
                            spellManager.resetInitialCooldown(spellCastManager.currentTurn)
            if Kernel().worker.contains("FightSpellCastFrame"):
                Kernel().worker.removeFrame(Kernel().worker.getFrame("FightSpellCastFrame"))
            # imf = Kernel().worker.getFrame("InventoryManagementFrame")
            # InventoryManager().shortcutBarSpells = imf.getWrappersFromShortcuts(sscmsg.shortcuts)
            return False

        elif isinstance(msg, SpellVariantActivationRequestAction):
            svara = msg
            svarmsg = SpellVariantActivationRequestMessage()
            svarmsg.init(svara.spellId)
            ConnectionsHandler()._conn.send(svarmsg)
            return True

        elif isinstance(msg, SpellVariantActivationMessage):
            svamsg = msg
            if svamsg.result:
                deactivatedSpellId = 0
                variants = SpellVariant.getSpellVariants()
                for variant in variants:
                    if svamsg.spellId not in variant.spellIds:
                        for spellIdInVariant in variant.spellIds:
                            if spellIdInVariant != svamsg.spellId:
                                deactivatedSpellId = spellIdInVariant
                for sw in self._fullSpellList[PlayedCharacterManager().id]:
                    if sw.spellId == svamsg.spellId and not sw.variantActivated:
                        sw.variantActivated = True
                    elif sw.spellId == deactivatedSpellId and sw.variantActivated:
                        sw.variantActivated = False
            return True

        elif isinstance(msg, FinishMoveListRequestAction):
            fmlrmsg = FinishMoveListRequestMessage()
            fmlrmsg.init()
            ConnectionsHandler()._conn.send(fmlrmsg)
            return True

        elif isinstance(msg, FinishMoveSetRequestAction):
            fmsra = msg
            for fmId in fmsra.enabledFinishedMoves:
                fmsrmsg = FinishMoveSetRequestMessage()
                fmsrmsg.init(fmId, True)
                ConnectionsHandler()._conn.send(fmsrmsg)
            for fmId in fmsra.disabledFinishedMoves:
                fmsrmsg = FinishMoveSetRequestMessage()
                fmsrmsg.init(fmId, False)
                ConnectionsHandler()._conn.send(fmsrmsg)
            return True

        elif isinstance(msg, FinishMoveListMessage):
            fmlmsg = msg
            finishMoves = []
            for fmi in fmlmsg.finishMoves:
                fm = FinishMove.getFinishMoveById(fmi.finishMoveId)
                finishMoves.append(
                    {
                        "id": fm.id,
                        "name": Spell.getSpellById(fm.getSpellLevel().spellId).name,
                        "enabled": fmi.finishMoveState,
                    }
                )
            finishMoves.sort(lambda e: e["id"])
            return True

        else:
            return False

    def pulled(self) -> bool:
        return True

    def getFullSpellListByOwnerId(self, ownerId: float) -> list:
        return self._fullSpellList[ownerId]

    def addSpellGlobalCoolDownInfo(self, pEntityId: float, pGameFightSpellCooldown: GameFightSpellCooldown) -> None:
        if not self._spellsGlobalCooldowns[pEntityId]:
            self._spellsGlobalCooldowns[pEntityId] = list[GameFightSpellCooldown](0)
        self._spellsGlobalCooldowns[pEntityId].append(pGameFightSpellCooldown)

    def applySpellGlobalCoolDownInfo(self, pEntityId: float) -> None:
        sgcds: list[GameFightSpellCooldown] = self._spellsGlobalCooldowns.get(pEntityId)
        if sgcds:
            for gfsc in sgcds:
                gcdvalue = gfsc.cooldown
                spellKnown = False
                for sw in self._fullSpellList[pEntityId]:
                    if sw.spellId == gfsc.spellId:
                        spellKnown = True
                        spellLevel = sw.spellLevel
                        if gcdvalue == -1:
                            gcdvalue = sw.spellLevelInfos.minCastInterval
                if spellKnown:
                    spellCastManager = CurrentPlayedFighterManager().getSpellCastManagerById(pEntityId)
                    if not spellCastManager.getSpellManagerBySpellId(gfsc.spellId):
                        spellCastManager.castSpell(gfsc.spellId, spellLevel, [], False)
                        spellManager = spellCastManager.getSpellManagerBySpellId(gfsc.spellId)
                        spellManager.forceCooldown(gcdvalue)
                    else:
                        spellManager = spellCastManager.getSpellManagerBySpellId(gfsc.spellId)
                        if spellManager.cooldown <= gcdvalue:
                            spellManager.forceCooldown(gcdvalue)
            sgcds.clear()
            del self._spellsGlobalCooldowns[pEntityId]

    def deleteSpellsGlobalCoolDownsData(self) -> None:
        id = None
        for id in self._spellsGlobalCooldowns:
            self._spellsGlobalCooldowns[id].length = 0
            del self._spellsGlobalCooldowns[id]

    def getBreedSpellsInVariantslist(self) -> list:
        # if FeatureManager().isFeatureWithKeywordEnabled(
        #     "character.spell.breed.alternative"
        # ):
        #     return self.generateCurrentCustomModeBreedSpells()
        playerBreedId: int = PlayedCharacterManager().infos.breed
        breedData: Breed = Breed.getBreedById(playerBreedId)
        breedSpellsId: list = breedData.allSpellsId
        spellsInventory: list = PlayedCharacterManager().spellsInventory
        spells: list = list()
        variantIdsPacks: list = list()
        spellWrappersById: dict = dict(True)
        processedVariantIds: list = list()
        for spellWrapper in spellsInventory:
            if spellWrapper.spell.id in breedSpellsId:
                spellWrappersById[spellWrapper.id] = spellWrapper
                spellVariant = spellWrapper.spell.spellVariant
                if spellVariant:
                    firstSpellId = spellVariant.spellIds[0]
                    if firstSpellId not in processedVariantIds:
                        processedVariantIds.append(firstSpellId)
                        variantIdsPacks.append(spellVariant.spellIds)
                else:
                    spellIdInVector = list[int]()
                    spellIdInVector.append(spellWrapper.id)
                    variantIdsPacks.append(spellIdInVector)
        for idsPack in variantIdsPacks:
            variants = list()
            for spellId in idsPack:
                if spellWrappersById[spellId]:
                    variants.append(spellWrappersById[spellId])
            spells.append(variants)
        spells.sort(key=cmp_to_key(self.sortOnObtentionLevel))
        return spells

    def getCommonSpellsInVariantslist(self) -> list:
        playerBreedId: int = PlayedCharacterManager().infos.breed
        _isForgettableSpellsUi: bool = False
        # FeatureManager().isFeatureWithKeywordEnabled(
        #     "character.spell.forgettable"
        # )
        if _isForgettableSpellsUi:
            breedSpellsId = CustomModeBreedSpell.getCustomModeBreedSpellIds(playerBreedId)
        else:
            breedData = Breed.getBreedById(playerBreedId)
            breedSpellsId = breedData.allSpellsId
        spellsInventory: list = PlayedCharacterManager().spellsInventory
        spells: list = list()
        variantIdsPacks: list = list()
        spellWrappersById: dict = dict(True)
        processedVariantIds: list = list()
        for spellWrapper in spellsInventory:
            isForgettableSpell = _isForgettableSpellsUi and SpellManager.isForgettableSpell(spellWrapper.spell.id)
            if not (spellWrapper.spell.id in breedSpellsId or isForgettableSpell):
                spellWrappersById[spellWrapper.id] = spellWrapper
                spellVariant = spellWrapper.spell.spellVariant
                if spellVariant:
                    firstSpellId = spellVariant.spellIds[0]
                    if firstSpellId not in processedVariantIds:
                        processedVariantIds.append(firstSpellId)
                        variantIdsPacks.append(spellVariant.spellIds)
                else:
                    spellIdInVector = list[int]()
                    spellIdInVector.append(spellWrapper.id)
                    variantIdsPacks.append(spellIdInVector)
        for idsPack in variantIdsPacks:
            variants = list()
            for spellId in idsPack:
                if spellWrappersById[spellId]:
                    variants.append(spellWrappersById[spellId])
            spells.append(variants)
        spells.sort(key=cmp_to_key(self.sortOnObtentionLevel))
        return spells

    def sortOnObtentionLevel(self, spellsA: object, spellsB: object) -> float:
        aObtentionLevel: int = spellsA[0].spell.getSpellLevel(0).minPlayerLevel
        bObtentionLevel: int = spellsB[0].spell.getSpellLevel(0).minPlayerLevel
        aObtentionLevelVariant1: int = 0
        if len(spellsA) > 1:
            aObtentionLevelVariant1 = spellsA[1].spell.getSpellLevel(0).minPlayerLevel
        bObtentionLevelVariant1: int = 0
        if len(spellsB) > 1:
            bObtentionLevelVariant1 = spellsB[1].spell.getSpellLevel(0).minPlayerLevel
        if aObtentionLevel > bObtentionLevel:
            return 1
        if aObtentionLevel < bObtentionLevel:
            return -1
        if aObtentionLevelVariant1 > bObtentionLevelVariant1:
            return 1
        if aObtentionLevelVariant1 < bObtentionLevelVariant1:
            return -1
        if spellsA[0].id > spellsB[0].id:
            return 1
        if spellsA[0].id < spellsB[0].id:
            return -1
        return 0
