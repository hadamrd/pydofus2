from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.berilia.interfaces.IApi import IApi
from pydofus2.com.ankamagames.dofus.datacenter.breeds.Breed import Breed
from pydofus2.com.ankamagames.dofus.datacenter.optionalFeatures.CustomModeBreedSpell import \
    CustomModeBreedSpell
from pydofus2.com.ankamagames.dofus.datacenter.optionalFeatures.ForgettableSpell import \
    ForgettableSpell
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.WeaponWrapper import \
    WeaponWrapper
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.network.enums.AlignmentSideEnum import \
    AlignmentSideEnum
from pydofus2.com.ankamagames.dofus.types.data.PlayerSetInfo import \
    PlayerSetInfo

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import (
        SpellWrapper,
    )

from pydofus2.com.ankamagames.dofus.internalDatacenter.mount.MountData import \
    MountData
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import \
    EntityStats
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import \
    WorldPointWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import \
    StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AbstractEntitiesFrame import \
    AbstractEntitiesFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import \
    InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightPreparationFrame import \
    FightPreparationFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
    CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import \
    SpellManager
from pydofus2.com.ankamagames.dofus.network.enums.CharacterInventoryPositionEnum import \
    CharacterInventoryPositionEnum
from pydofus2.com.ankamagames.dofus.network.enums.PlayerLifeStatusEnum import \
    PlayerLifeStatusEnum
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import \
    CharacterCharacteristicsInformations
from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.CharacterBaseInformations import \
    CharacterBaseInformations
from pydofus2.com.ankamagames.dofus.network.types.game.character.restriction.ActorRestrictionsInformations import \
    ActorRestrictionsInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
    GameRolePlayActorInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayCharacterInformations import \
    GameRolePlayCharacterInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayMutantInformations import \
    GameRolePlayMutantInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GuildInformations import \
    GuildInformations
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ForgettableSpellItem import \
    ForgettableSpellItem
from pydofus2.com.ankamagames.dofus.network.types.game.guild.application.GuildApplicationInformation import \
    GuildApplicationInformation


class PlayedCharacterInfo(object):
    def __init__(self, i: CharacterBaseInformations) -> None:
        self.id = i.id
        self.breed = i.breed
        self.level = i.level
        self.limitedLevel = PlayedCharacterManager().limitedLevel
        self.sex = i.sex
        self.name = i.name


class PlayedCharacterApi(IApi):
    @classmethod
    def characteristics(cls) -> CharacterCharacteristicsInformations:
        return PlayedCharacterManager().characteristics

    @classmethod
    def canRideMount(cls) -> bool:
        return not PlayerManager().isBasicAccount() and PlayedCharacterApi.getMount() and not PlayedCharacterApi.isRiding() and PlayedCharacterApi.mountLeftEnergyRatio() > 0.05
    
    @classmethod
    def stats(cls) -> EntityStats:
        return StatsManager().getStats(PlayedCharacterManager().id)

    @classmethod
    def getPlayedCharacterInfo(cls) -> PlayedCharacterInfo:
        i: CharacterBaseInformations = PlayedCharacterManager().infos
        if not i:
            return None
        return PlayedCharacterInfo(i)

    @classmethod
    def getInventory(cls) -> list[ItemWrapper]:
        return InventoryManager().realInventory

    @classmethod
    def getEquipment(cls) -> list:
        item = None
        equipment: list = list()
        for item in PlayedCharacterManager().inventory:
            if item.position <= CharacterInventoryPositionEnum.ACCESSORY_POSITION_SHIELD:
                equipment.append(item)
        return equipment

    @classmethod
    def getSpellInventory(cls) -> list["SpellWrapper"]:
        return PlayedCharacterManager().spellsInventory

    @classmethod
    def getSpells(cls, returnBreedSpells: bool) -> list:
        spim = Kernel().spellInventoryManagementFrame
        if returnBreedSpells:
            return spim.getBreedSpellsInVariantslist()
        return spim.getCommonSpellsInVariantslist()

    @classmethod
    def getPlayerForgettableSpells(cls) -> dict:
        return PlayedCharacterManager().playerForgettableSpelldict

    @classmethod
    def getPlayerMaxForgettableSpellsNumber(cls) -> int:
        return PlayedCharacterManager().playerMaxForgettableSpellsNumber

    @classmethod
    def getForgettableSpells(cls) -> list:
        return ForgettableSpell.getForgettableSpells()

    @classmethod
    def getForgettableSpellById(cls, id: int) -> ForgettableSpell:
        return ForgettableSpell.getForgettableSpellById(id)

    @classmethod
    def isForgettableSpellAvailable(cls, id: int) -> bool:
        forgettableSpellItems: dict = PlayedCharacterManager().playerForgettableSpelldict
        if forgettableSpellItems == None:
            return False
        forgettableSpellItem: ForgettableSpellItem = forgettableSpellItems[id]
        if forgettableSpellItem == None:
            return False
        return forgettableSpellItem.available

    @classmethod
    def isForgettableSpell(cls, spellId: int) -> bool:
        return SpellManager.isForgettableSpell(spellId)

    @classmethod
    def getCustomModeBreedSpellById(cls, id: int) -> CustomModeBreedSpell:
        return CustomModeBreedSpell.getCustomModeBreedSpellById(id)

    @classmethod
    def getCustomModeSpellIds(cls) -> list[int]:
        return CustomModeBreedSpell.getAllCustomModeBreedSpellIds()

    @classmethod
    def getCustomModeBreedSpellList(cls, breedId: int) -> list:
        return CustomModeBreedSpell.getCustomModeBreedSpellList(breedId)

    @classmethod
    def getBreedSpellActivatedIds(cls) -> list:
        spellsInventory = PlayedCharacterManager().spellsInventory
        activatedSpellIds = list()
        playerBreedId = PlayedCharacterManager().infos.breed
        breedData = Breed.getBreedById(playerBreedId)
        breedSpellsId = breedData.allSpellsId
        for spellWrapper in spellsInventory:
            if spellWrapper is not None:
                if spellWrapper.variantActivated and breedSpellsId.find(spellWrapper.id) != -1:
                    activatedSpellIds.append(spellWrapper.id)
        return activatedSpellIds

    @classmethod
    def getMount(cls) -> MountData:
        return PlayedCharacterManager().mount

    @classmethod
    def getPetsMount(cls) -> ItemWrapper:
        return PlayedCharacterManager().petsMount

    @classmethod
    def getKnownTitles(cls) -> list[int]:
        return Kernel().worker.getFrameByName("TinselFrame").knownTitles

    @classmethod
    def getKnownOrnaments(cls) -> list[int]:
        return Kernel().worker.getFrameByName("TinselFrame").knownOrnaments

    @classmethod
    def titlesOrnamentsAskedBefore(cls) -> bool:
        return Kernel().worker.getFrameByName("TinselFrame").titlesOrnamentsAskedBefore

    @classmethod
    def getEntityInfos(cls) -> GameRolePlayCharacterInformations:
        entitiesFrame: AbstractEntitiesFrame = None
        if cls.isInFight():
            entitiesFrame = Kernel().fightEntitiesFrame
        else:
            entitiesFrame = Kernel().roleplayEntitiesFrame
        if not entitiesFrame:
            return None
        return entitiesFrame.getEntityInfos(PlayedCharacterManager().id)

    @classmethod
    def getKamasMaxLimit(cls) -> float:
        playedCharacterFrame = Kernel().playedCharacterUpdatesFrame
        if playedCharacterFrame:
            return playedCharacterFrame.kamasLimit
        return 0

    @classmethod
    def inventoryWeight(cls) -> int:
        return PlayedCharacterManager().inventoryWeight

    @classmethod
    def shopWeight(cls) -> int:
        return PlayedCharacterManager().shopWeight

    @classmethod
    def inventoryWeightMax(cls) -> int:
        return PlayedCharacterManager().inventoryWeightMax

    @classmethod
    def isIncarnation(cls) -> bool:
        return PlayedCharacterManager().isIncarnation

    @classmethod
    def isMutated(cls) -> bool:
        return PlayedCharacterManager().isMutated

    @classmethod
    def isInHouse(cls) -> bool:
        return PlayedCharacterManager().isInHouse

    @classmethod
    def isIndoor(cls) -> bool:
        return PlayedCharacterManager().isIndoor

    @classmethod
    def isInExchange(cls) -> bool:
        return PlayedCharacterManager().isInExchange

    @classmethod
    def isInFight(cls) -> bool:
        return Kernel().worker.contains("FightContextFrame")

    @classmethod
    def isInPreFight(cls) -> bool:
        return Kernel().worker.contains("FightPreparationFrame") or Kernel().worker.isBeingAdded(FightPreparationFrame)

    @classmethod
    def isSpectator(cls) -> bool:
        return PlayedCharacterManager().isSpectator

    @classmethod
    def isInParty(cls) -> bool:
        return PlayedCharacterManager().isInParty

    @classmethod
    def isPartyLeader(cls) -> bool:
        return PlayedCharacterManager().isPartyLeader

    @classmethod
    def isRiding(cls) -> bool:
        return PlayedCharacterManager().isRiding

    @classmethod
    def isPetsMounting(cls) -> bool:
        return PlayedCharacterManager().isPetsMounting

    @classmethod
    def hasCompanion(cls) -> bool:
        return PlayedCharacterManager().hasCompanion

    @classmethod
    def id(cls) -> float:
        return PlayedCharacterManager().id

    @classmethod
    def restrictions(cls) -> ActorRestrictionsInformations:
        return PlayedCharacterManager().restrictions

    @classmethod
    def isMutant(cls) -> bool:
        rcf = Kernel().roleplayContextFrame
        infos: GameRolePlayActorInformations = rcf.entitiesFrame.getEntityInfos(PlayedCharacterManager().id)
        return infos is GameRolePlayMutantInformations

    @classmethod
    def publicMode(cls) -> bool:
        return PlayedCharacterManager().publicMode

    @classmethod
    def artworkId(cls) -> int:
        return PlayedCharacterManager().artworkId

    @classmethod
    def getAlignmentSide(cls) -> int:
        if PlayedCharacterManager().characteristics:
            return PlayedCharacterManager().characteristics.alignmentInfos.alignmentSide
        return AlignmentSideEnum.ALIGNMENT_NEUTRAL

    @classmethod
    def getAlignmentValue(cls) -> int:
        return PlayedCharacterManager().characteristics.alignmentInfos.alignmentValue

    @classmethod
    def getAlignmentAggressableStatus(cls) -> int:
        return PlayedCharacterManager().characteristics.alignmentInfos.aggressable

    @classmethod
    def getAlignmentGrade(cls) -> int:
        return PlayedCharacterManager().characteristics.alignmentInfos.alignmentGrade

    @classmethod
    def getMaxSummonedCreature(cls) -> int:
        return CurrentPlayedFighterManager().getMaxSummonedCreature()

    @classmethod
    def getCurrentSummonedCreature(cls) -> int:
        return CurrentPlayedFighterManager().getCurrentSummonedCreature()

    @classmethod
    def canSummon(cls) -> bool:
        return CurrentPlayedFighterManager().canSummon()

    @classmethod
    def getSpell(cls, spellId: int) -> "SpellWrapper":
        return CurrentPlayedFighterManager().getSpellById(spellId)

    @classmethod
    def canCastThisSpell(cls, spellId: int, lvl: int) -> bool:
        return CurrentPlayedFighterManager().canCastThisSpell(spellId, lvl)

    @classmethod
    def canCastThisSpellWithResult(cls, spellId: int, lvl: int, target: float = 0) -> str:
        canCast, reason = CurrentPlayedFighterManager().canCastThisSpell(spellId, lvl, target)
        return reason

    @classmethod
    def canCastThisSpellOnTarget(cls, spellId: int, lvl: int, pTargetId: float) -> bool:
        canCast, reason = CurrentPlayedFighterManager().canCastThisSpell(spellId, lvl, pTargetId)
        return canCast

    @classmethod
    def isInHisHouse(cls) -> bool:
        return PlayedCharacterManager().isInHisHouse

    # def getPlayerHouses(cls) -> list[HouseWrapper]:
    #     return Kernel().worker.getFrame("HouseFrame").accountHouses

    @classmethod
    def currentMap(cls) -> WorldPointWrapper:
        return PlayedCharacterManager().currentMap

    @classmethod
    def previousMap(cls) -> WorldPointWrapper:
        return PlayedCharacterManager().previousMap

    @classmethod
    def previousWorldMapId(cls) -> int:
        return PlayedCharacterManager().previousWorldMapId

    @classmethod
    def previousSubArea(cls) -> SubArea:
        return PlayedCharacterManager().previousSubArea

    @classmethod
    def currentSubArea(cls) -> SubArea:
        return PlayedCharacterManager().currentSubArea

    @classmethod
    def isInTutorialArea(cls) -> bool:
        subarea: SubArea = PlayedCharacterManager().currentSubArea
        return subarea and subarea.id == DataEnum.SUBAREA_TUTORIAL

    @classmethod
    def state(cls) -> int:
        return PlayedCharacterManager().state

    @classmethod
    def isAlive(cls) -> bool:
        return PlayedCharacterManager().state == PlayerLifeStatusEnum.STATUS_ALIVE_AND_KICKING

    @classmethod
    def getFollowingPlayerIds(cls) -> list[float]:
        return PlayedCharacterManager().followingPlayerIds

    @classmethod
    def getPlayerSet(cls, objectGID: int) -> PlayerSetInfo:
        return Kernel().playedCharacterUpdatesFrame.getPlayerSet(objectGID)

    @classmethod
    def getWeapon(cls) -> WeaponWrapper:
        if InventoryManager().currentBuildId != -1:
            for build in InventoryManager().builds:
                if build.id == InventoryManager().currentBuildId:
                    break
            for iw in build.equipment:
                if isinstance(iw, WeaponWrapper):
                    break
            if iw:
                return iw
            return None
        return PlayedCharacterManager().currentWeapon

    @classmethod
    def getExperienceBonusPercent(cls) -> int:
        return PlayedCharacterManager().experiencePercent

    @classmethod
    def getAchievementPoints(cls) -> int:
        return PlayedCharacterManager().achievementPoints

    @classmethod
    def getWaitingGifts(cls) -> list:
        return PlayedCharacterManager().waitingGifts

    @classmethod
    def isInHisHavenbag(cls) -> bool:
        return PlayedCharacterManager().isInHisHavenbag

    @classmethod
    def isInHavenbag(cls) -> bool:
        return PlayedCharacterManager().isInHavenbag

    @classmethod
    def havenbagSharePermissions(cls) -> int:
        hbFrame = Kernel().worker.getFrameByName("HavenbagFrame")
        return hbFrame.sharePermissions

    @classmethod
    def isInBreach(cls) -> bool:
        return PlayedCharacterManager().isInBreach

    @classmethod
    def isInBreachSubArea(cls) -> bool:
        return PlayedCharacterManager().currentSubArea.id == 904 or PlayedCharacterManager().currentSubArea.id == 938

    @classmethod
    def isInAnomaly(cls) -> bool:
        return PlayedCharacterManager().isInAnomaly

    @classmethod
    def getApplicationInfo(cls) -> GuildApplicationInformation:
        return PlayedCharacterManager().applicationInfo
    
    @classmethod
    def inventoryKamas(cls) -> int:
        return InventoryManager().inventory.kamas

    @classmethod
    def getGuildApplicationInfo(cls) -> GuildInformations:
        return PlayedCharacterManager().guildApplicationInfo

    @classmethod
    def getPlayerApplicationInformation(cls) -> object:
        class o:
            pass

        o.guildInfo = PlayedCharacterManager().guildApplicationInfo
        o.applicationInfo = PlayedCharacterManager().applicationInfo
        return o

    @classmethod
    def isInKoli(cls) -> bool:
        return PlayedCharacterManager().isInKoli
    
    @classmethod
    def mountLeftEnergyRatio(cls) -> float:
        mount = cls.getMount()
        if mount is None:
            return None
        return mount.energy / mount.energyMax
