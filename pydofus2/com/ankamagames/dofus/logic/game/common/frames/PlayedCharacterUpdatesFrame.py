from datetime import datetime
from logging import Logger
from time import perf_counter
from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper as swmod
import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
import pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayContextFrame as rplCF
from pydofus2.com.ankamagames.dofus.datacenter.breeds.Breed import Breed
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimerManager import TimeManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
from pydofus2.com.ankamagames.dofus.network.enums.AggressableStatusEnum import AggressableStatusEnum
from pydofus2.com.ankamagames.dofus.network.enums.GameServerTypeEnum import GameServerTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.PlayerLifeStatusEnum import PlayerLifeStatusEnum
from pydofus2.com.ankamagames.dofus.network.enums.StatsUpgradeResultEnum import StatsUpgradeResultEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.almanach.AlmanachCalendarDateMessage import (
    AlmanachCalendarDateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.atlas.compass.CompassResetMessage import CompassResetMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.atlas.compass.CompassUpdatePartyMemberMessage import (
    CompassUpdatePartyMemberMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.atlas.compass.CompassUpdatePvpSeekMessage import (
    CompassUpdatePvpSeekMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.BasicTimeMessage import BasicTimeMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.debt.DebtsDeleteMessage import DebtsDeleteMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.debt.DebtsUpdateMessage import DebtsUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.spell.forgettable.ForgettableSpellDeleteMessage import (
    ForgettableSpellDeleteMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.spell.forgettable.ForgettableSpellEquipmentSlotsMessage import (
    ForgettableSpellEquipmentSlotsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.spell.forgettable.ForgettableSpellListUpdateMessage import (
    ForgettableSpellListUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.CharacterExperienceGainMessage import (
    CharacterExperienceGainMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.CharacterLevelUpMessage import CharacterLevelUpMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.CharacterStatsListMessage import (
    CharacterStatsListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapSpeedMovementMessage import GameMapSpeedMovementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.death.GameRolePlayGameOverMessage import (
    GameRolePlayGameOverMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.death.GameRolePlayPlayerLifeStatusMessage import (
    GameRolePlayPlayerLifeStatusMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.stats.StatsUpgradeResultMessage import (
    StatsUpgradeResultMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.initialization.CharacterCapabilitiesMessage import (
    CharacterCapabilitiesMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.initialization.ServerExperienceModificatorMessage import (
    ServerExperienceModificatorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.initialization.SetCharacterRestrictionsMessage import (
    SetCharacterRestrictionsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.interactive.zaap.KnownZaapListMessage import KnownZaapListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMoneyMovementInformationMessage import (
    ExchangeMoneyMovementInformationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.SetUpdateMessage import SetUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.startup.StartupActionAddMessage import StartupActionAddMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.startup.StartupActionFinishedMessage import (
    StartupActionFinishedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.startup.StartupActionsListMessage import StartupActionsListMessage
from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import (
    CharacterCharacteristicsInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionAlliance import HumanOptionAlliance
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanOptionOrnament import HumanOptionOrnament
from pydofus2.com.ankamagames.dofus.types.data.PlayerSetInfo import PlayerSetInfo
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.damageCalculation.tools.StatIds import StatIds

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import FightBattleFrame
    from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.RoleplayEntitiesFrame import RoleplayEntitiesFrame
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayHumanoidInformations import (
        GameRolePlayHumanoidInformations,
    )

logger = Logger("Dofus2")


class PlayedCharacterUpdatesFrame(Frame):

    SPELL_TOOLTIP_CACHE_NUM: int = 0

    FORGETTABLE_SPELL_FIRST_NOTIF_NAME: str = "firstForgettableSpell"

    setList: dict = {}

    guildEmblemSymbolCategories: int

    _kamasLimit: float

    _giftListInitialized: bool

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def roleplayContextFrame(self) -> rplCF.RoleplayContextFrame:
        return krnl.Kernel().worker.getFrame("RoleplayContextFrame")

    @property
    def kamasLimit(self) -> float:
        return self._kamasLimit

    def pushed(self) -> bool:
        self.setList = dict()
        self._giftListInitialized = False
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, SetCharacterRestrictionsMessage):
            scrmsg = msg
            if scrmsg.actorId == pcm.PlayedCharacterManager().id:
                pcm.PlayedCharacterManager().restrictions = scrmsg.restrictions
            rpEntitiesFrame: "RoleplayEntitiesFrame" = krnl.Kernel().worker.getFrame("RoleplayEntitiesFrame")
            if rpEntitiesFrame:
                infos: "GameRolePlayHumanoidInformations" = rpEntitiesFrame.getEntityInfos(scrmsg.actorId)
                if infos and infos.humanoidInfo:
                    infos.humanoidInfo.restrictions = scrmsg.restrictions
            return True

        if isinstance(msg, ServerExperienceModificatorMessage):
            semsg = msg
            pcm.PlayedCharacterManager().experiencePercent = semsg.experiencePercent - 100
            return True

        if isinstance(msg, CharacterStatsListMessage):
            cslmsg = msg
            fightBattleFrame: "FightBattleFrame" = krnl.Kernel().worker.getFrame("FightBattleFrame")
            if fightBattleFrame is not None and fightBattleFrame.executingSequence:
                fightBattleFrame.delayCharacterStatsList(cslmsg)
            else:
                self.updateCharacterStatsList(cslmsg.stats)
            if self.roleplayContextFrame and self.roleplayContextFrame.entitiesFrame:
                playerInfos = self.roleplayContextFrame.entitiesFrame.getEntityInfos(pcm.PlayedCharacterManager().id)
                if playerInfos:
                    playerInfos.alignmentInfos = cslmsg.stats.alignmentInfos
            if krnl.Kernel().worker.getFrame("QuestFrame"):
                if krnl.Kernel().worker.getFrame("QuestFrame").achievmentsListProcessed == False:
                    krnl.Kernel().worker.getFrame("QuestFrame")
            return False

        if isinstance(msg, MapComplementaryInformationsDataMessage):
            mcidmsg = msg
            for grai in mcidmsg.actors:
                grpci = grai
                if grpci and grpci.contextualId == pcm.PlayedCharacterManager().id:
                    pcm.PlayedCharacterManager().infos.entityLook = grpci.look
                    for opt in grpci.humanoidInfo.options:
                        if isinstance(opt, HumanOptionAlliance):
                            pcm.PlayedCharacterManager().characteristics.alignmentInfos.aggressable = opt.aggressable
            if not (
                pcm.PlayedCharacterManager().characteristics.alignmentInfos.aggressable
                == AggressableStatusEnum.AvA_DISQUALIFIED
                or pcm.PlayedCharacterManager().characteristics.alignmentInfos.aggressable
                == AggressableStatusEnum.AvA_ENABLED_AGGRESSABLE
                or pcm.PlayedCharacterManager().characteristics.alignmentInfos.aggressable
                == AggressableStatusEnum.AvA_ENABLED_NON_AGGRESSABLE
                or pcm.PlayedCharacterManager().characteristics.alignmentInfos.aggressable
                == AggressableStatusEnum.AvA_PREQUALIFIED_AGGRESSABLE
            ):
                return False

            SubArea.getSubAreaByMapId(mcidmsg.mapId)

            # if pcm.PlayedCharacterManager().currentSubArea and newSubArea:
            #    if PrismSubAreaWrapper.prismList[newSubArea.id]:
            #       prism = PrismSubAreaWrapper.prismList[newSubArea.id]
            #       if prism.state == PrismStateEnum.PRISM_STATE_VULNERABLE:
            #          if krnl.Kernel().worker.contains(AllianceFrame):
            #             allianceFrame = krnl.Kernel().worker.getFrame("AllianceFrame")

            return False

        if isinstance(msg, CharacterCapabilitiesMessage):
            ccmsg = msg
            self.guildEmblemSymbolCategories = ccmsg.guildEmblemSymbolCategories
            return True

        # if isinstance(msg, ResetCharacterStatsRequestAction):
        #    rcsra = msg
        #    rcsrmsg = ResetCharacterStatsRequestMessage()
        #    rcsrmsg.initResetCharacterStatsRequestMessage()
        #    ConnectionsHandler().conn.send(rcsrmsg)
        #    return True

        # if isinstance(msg, StatsUpgradeRequestAction):
        #    sura = msg
        #    surqmsg = StatsUpgradeRequestMessage()
        #    surqmsg.initStatsUpgradeRequestMessage(sura.useAdditionnal,sura.statId,sura.boostPoint)
        #    ConnectionsHandler().conn.send(surqmsg)
        #    return True

        if isinstance(msg, StatsUpgradeResultMessage):
            surmsg = msg
            if surmsg.result == StatsUpgradeResultEnum.SUCCESS:
                pass
            return True

        if isinstance(msg, CharacterLevelUpMessage):
            clumsg = msg
            entityInfos = None
            previousLevel = pcm.PlayedCharacterManager().infos.level
            pcm.PlayedCharacterManager().infos.level = clumsg.newLevel
            if clumsg.newLevel == 10 and PlayerManager().server.gameTypeId != GameServerTypeEnum.SERVER_TYPE_TEMPORIS:
                newSpellWrappers = []
                playerBreed = Breed.getBreedById(pcm.PlayedCharacterManager().infos.breed)
                for spellVariant in playerBreed.breedSpellVariants:
                    for spellBreed in spellVariant.spells:
                        for spellLevelBreedId in spellBreed.spellLevels:
                            spellLevelBreed = SpellLevel.getLevelById(spellLevelBreedId)
                            if spellLevelBreed:
                                obtentionLevel = spellLevelBreed.minPlayerLevel
                                if obtentionLevel <= clumsg.newLevel and obtentionLevel > previousLevel:
                                    newSpellWrappers.append(
                                        swmod.SpellWrapper.create(spellBreed.id, spellLevelBreed.grade, False)
                                    )
                for spellWrapper in pcm.PlayedCharacterManager().spellsInventory:
                    spellWrapper.updateSpellLevelAndEffectsAccordingToPlayerLevel()

                if self.roleplayContextFrame:
                    entityInfos = self.roleplayContextFrame.entitiesFrame.getEntityInfos(
                        pcm.PlayedCharacterManager().id
                    )

                if entityInfos:
                    for option in entityInfos.humanoidInfo.options:
                        if isinstance(option, HumanOptionOrnament):
                            option.level = clumsg.newLevel

            return False

        if isinstance(msg, CharacterExperienceGainMessage):
            return True

        if isinstance(msg, GameRolePlayPlayerLifeStatusMessage):
            grplsmsg = msg
            state = PlayerLifeStatusEnum(grplsmsg.state)
            pcm.PlayedCharacterManager().state = state
            logger.debug(f"Player state is {state.name}")
            return False

        if isinstance(msg, GameRolePlayGameOverMessage):
            pcm.PlayedCharacterManager().state = PlayerLifeStatusEnum.STATUS_TOMBSTONE
            return True

        if isinstance(msg, AlmanachCalendarDateMessage):
            # acdmsg = msg
            # AlmanaxManager().calendar = AlmanaxCalendar.getAlmanaxCalendarById(acdmsg.date)
            return True

        if isinstance(msg, SetUpdateMessage):
            sumsg = msg
            self.setList[sumsg.setId] = PlayerSetInfo(sumsg.setId, sumsg.setObjects, sumsg.setEffects)
            return True

        if isinstance(msg, CompassResetMessage):
            # crmsg = msg
            # name = "flag_srv" + crmsg.type

            # if crmsg.type  == CompassTypeEnum.COMPASS_TYPE_SPOUSE:
            #    socialFrame = krnl.Kernel().worker.getFrame("SocialFrame")
            #    socialFrame.spouse.followSpouse = False

            # if crmsg.type  == CompassTypeEnum.COMPASS_TYPE_PARTY:
            #    pcm.PlayedCharacterManager().followingPlayerIds = []
            #    return True
            return True

        if isinstance(msg, CompassUpdatePartyMemberMessage):
            pass

        if isinstance(msg, CompassUpdatePvpSeekMessage):
            pass

        if isinstance(msg, BasicTimeMessage):
            btmsg = msg
            receptionDelay = perf_counter() - btmsg.receptionTime
            TimeManager().serverTimeLag = (
                btmsg.timestamp + btmsg.timezoneOffset * 60 * 1000 - datetime.now().timestamp() + receptionDelay
            )
            TimeManager().serverUtcTimeLag = btmsg.timestamp - datetime.now().timestamp() + receptionDelay
            return True

        if isinstance(msg, StartupActionsListMessage):
            # salm = msg
            # giftList = []
            # initialGiftCount = 0
            # if pcm.PlayedCharacterManager().waitingGifts and pcm.PlayedCharacterManager().len(waitingGifts) != 0:
            #    initialGiftCount = pcm.PlayedCharacterManager().len(waitingGifts)
            # for gift in salm.actions:
            #        _items = []
            #    for item in gift.items:
            #       iw = ItemWrapper.create(0,0,item.objectGID,item.quantity,item.effects,False)
            #       _items.append(iw)
            #       obj = {
            #          "uid":gift.uid,
            #          "title":gift.title,
            #          "text":gift.text,
            #          "items":_items
            #       }
            #    giftList.append(obj)
            # pcm.PlayedCharacterManager().waitingGifts = giftList
            # if len(giftList) > 0:
            #    if self._giftListInitialized and len(giftList) != initialGiftCount and len(giftList) > initialGiftCount:
            #       pass
            # self._giftListInitialized = True
            return True

        if isinstance(msg, StartupActionAddMessage):
            # saam = msg
            # items = []
            # for itema in saam.newAction.items:
            #    iw = ItemWrapper.create(0,0,itema.objectGID,itema.quantity,itema.effects,False)
            #    items.append(iw)
            # obj = {
            #    "uid":saam.newAction.uid,
            #    "title":saam.newAction.title,
            #    "text":saam.newAction.text,
            #    "items":items
            # }
            # pcm.PlayedCharacterManager().waitingGifts.append(obj)
            return True

        # if isinstance(msg, GiftAssignRequestAction):
        #    gar = msg
        #    sao = StartupActionsObjetAttributionMessage()
        #    sao.initStartupActionsObjetAttributionMessage(gar.giftId,gar.characterId)
        #    ConnectionsHandler().conn.send(sao)
        #    return True

        # if isinstance(msg, GiftAssignAllRequestAction):
        #    gaara = msg
        #    saaamsg = StartupActionsAllAttributionMessage()
        #    saaamsg.initStartupActionsAllAttributionMessage(gaara.characterId)
        #    ConnectionsHandler().conn.send(saaamsg)
        #    return True

        if isinstance(msg, StartupActionFinishedMessage):
            # safm = msg
            # indexToDelete = -1
            # for giftAction in pcm.PlayedCharacterManager().waitingGifts:
            #    if giftAction.uid == safm.actionId:
            #       indexToDelete = pcm.PlayedCharacterManager().waitingGifts.find(giftAction)
            # if indexToDelete > -1:
            #    pcm.PlayedCharacterManager().waitingGifts.splice(indexToDelete,1)
            #    if len(pcm.PlayedCharacterManager().waitingGifts) == 0:
            #       pass
            return True

        if isinstance(msg, ExchangeMoneyMovementInformationMessage):
            emmim = msg
            self._kamasLimit = emmim.limit
            return True

        if isinstance(msg, DebtsUpdateMessage):
            pass
            # DebtManager().updateDebts(dum.debts)
            return True

        if isinstance(msg, DebtsDeleteMessage):
            pass
            # DebtManager().removeDebts(ddm.debts)
            return True

        if isinstance(msg, ForgettableSpellListUpdateMessage):
            # fslumsg = msg
            # if fslumsg.action == ForgettableSpellListActionEnum.FORGETTABLE_SPELL_LIST_DISPATCH:
            #    newSpellList = dict()
            #    for forgettableSpell in fslumsg.spells:
            #       newSpellList[forgettableSpell.spellId] = forgettableSpell
            #    pcm.PlayedCharacterManager().playerForgettableSpelldict = newSpellList
            # else:
            #    ds = DataStoreType("AccountModule_",True,DataStoreEnum.LOCATION_LOCAL,DataStoreEnum.BIND_ACCOUNT)
            #    if not StoreDataManager().getData(ds,FORGETTABLE_SPELL_FIRST_NOTIF_NAME):
            #       StoreDataManager().setData(ds,FORGETTABLE_SPELL_FIRST_NOTIF_NAME,True)
            #       nid = NotificationManager().prepareNotification(I18n.getUiText("ui.temporis.popupFirstSpellAddedTitle"),I18n.getUiText("ui.temporis.popupFirstSpellAddedContent"),NotificationTypeEnum.TUTORIAL,"FirstForgettableSpellNotif")
            #       NotificationManager().addButtonToNotification(nid,I18n.getUiText("ui.temporis.popupFirstSpellAddedButton"),"OpenForgettableSpellsUiAction")
            #       NotificationManager().sendNotification(nid)
            #    playerForgettableSpellsDict = pcm.PlayedCharacterManager().playerForgettableSpelldict
            #    for forgettableSpell in fslumsg.spells:
            #       playerForgettableSpellsDict[forgettableSpell.spellId] = forgettableSpell
            # KernelEventsManager().processCallback(HookList.ForgettableSpellListUpdate)
            # StorageOptionManager().updateStorageView()
            # InventoryManager().inventory.releaseHooks()
            return True

        if isinstance(msg, ForgettableSpellDeleteMessage):
            # fsdmsg = msg
            # playerForgettableSpellsDict = pcm.PlayedCharacterManager().playerForgettableSpelldict
            # for forgettableSpellId in fsdmsg.spells:
            #    del playerForgettableSpellsDict[forgettableSpellId]
            # StorageOptionManager().updateStorageView()
            # InventoryManager().inventory.releaseHooks()
            return True

        if isinstance(msg, ForgettableSpellEquipmentSlotsMessage):
            # fsesmsg = msg
            # pcm.PlayedCharacterManager().playerMaxForgettableSpellsfloat = fsesmsg.quantity
            return True

        if isinstance(msg, KnownZaapListMessage):
            kzlmsg = msg
            pcm.PlayedCharacterManager().updateKnownZaaps(kzlmsg.destinations)
            return True

        # if isinstance(msg, UpdateSpellModifierAction):
        #    usmaction = msg
        #    self.updateSpellModifier(usmaction.entityId,usmaction.spellId,usmaction.statId)
        #    return True

        if isinstance(msg, GameMapSpeedMovementMessage):
            gmsmm = msg
            newSpeedAjust = 10 * (gmsmm.speedMultiplier - 1)
            pcm.PlayedCharacterManager().speedAjust = newSpeedAjust
            if (
                DofusEntities.getEntity(pcm.PlayedCharacterManager().id) is not None
                and self.roleplayContextFrame is not None
            ):
                DofusEntities.getEntity(pcm.PlayedCharacterManager().id).speedAdjust = newSpeedAjust
            return True

        return False

    def updateCharacterStatsList(self, stats: CharacterCharacteristicsInformations) -> None:
        playerId: float = pcm.PlayedCharacterManager().id
        statsManager: StatsManager = StatsManager()
        playerStats: EntityStats = statsManager.getStats(playerId)
        if playerStats is not None:
            playerStats.getStatTotalValue(StatIds.ENERGY_POINTS)
        statsManager.addRawStats(playerId, stats.characteristics)
        SpellModifiersManager().setRawSpellsModifiers(playerId, stats.spellModifications)
        if stats.kamas != InventoryManager().inventory.kamas:
            InventoryManager().inventory.kamas = stats.kamas
        pcm.PlayedCharacterManager().characteristics = stats
        if pcm.PlayedCharacterManager().isFighting:
            if CurrentPlayedFighterManager().isRealPlayer():
                pass
            swmod.SpellWrapper.refreshAllPlayerSpellHolder(pcm.PlayedCharacterManager().id)
        else:
            pass

    def updateSpellModifier(self, targetId: float, spellId: float, statId: float) -> None:
        playerId: float = pcm.PlayedCharacterManager().id
        if playerId is not targetId:
            return
        spell = swmod.SpellWrapper.getSpellWrapperById(spellId, playerId)
        if spell is not None:
            spell = spell.clone()
            ++spell.versionNum

    def pulled(self) -> bool:
        return True
