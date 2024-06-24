import math

import pydofus2.com.ankamagames.atouin.managers.MapDisplayManager as mdm
import pydofus2.com.ankamagames.dofus.datacenter.spells.Spell as spellmod
from pydofus2.com.ankamagames.atouin.managers.EntitiesManager import EntitiesManager
from pydofus2.com.ankamagames.atouin.messages.MapLoadedMessage import MapLoadedMessage
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.challenges.Challenge import Challenge
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Companion import Companion
from pydofus2.com.ankamagames.dofus.datacenter.monsters.Monster import Monster
from pydofus2.com.ankamagames.dofus.datacenter.npcs.TaxCollectorFirstname import TaxCollectorFirstname
from pydofus2.com.ankamagames.dofus.datacenter.npcs.TaxCollectorName import TaxCollectorName
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.ChallengeWrapper import ChallengeWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.EmptyChallengerWrapper import EmptyChallengeWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.FightResultEntryWrapper import FightResultEntryWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import WorldPointWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InactivityManager import InactivityManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.messages.FightEndingMessage import FightEndingMessage
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.ChallengeTargetsListRequestAction import (
    ChallengeTargetsListRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.UpdateSpellModifierAction import UpdateSpellModifierAction
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightBattleFrame import FightBattleFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import FightEntitiesFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightPreparationFrame import FightPreparationFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager import BuffManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.dofus.network.enums.ChallengeBonusEnum import ChallengeBonusEnum
from pydofus2.com.ankamagames.dofus.network.enums.ChallengeModEnum import ChallengeModEnum
from pydofus2.com.ankamagames.dofus.network.enums.ChallengeStateEnum import ChallengeStateEnum
from pydofus2.com.ankamagames.dofus.network.enums.CharacterSpellModificationTypeEnum import (
    CharacterSpellModificationTypeEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.FightOutcomeEnum import FightOutcomeEnum
from pydofus2.com.ankamagames.dofus.network.enums.FightTypeEnum import FightTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.MapObstacleStateEnum import MapObstacleStateEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightNoSpellCastMessage import (
    GameActionFightNoSpellCastMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.arena.ArenaFighterIdleMessage import (
    ArenaFighterIdleMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.arena.ArenaFighterLeaveMessage import (
    ArenaFighterLeaveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.breach.BreachGameFightEndMessage import (
    BreachGameFightEndMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeAddMessage import (
    ChallengeAddMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeBonusChoiceMessage import (
    ChallengeBonusChoiceMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeBonusChoiceSelectedMessage import (
    ChallengeBonusChoiceSelectedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeInfoMessage import (
    ChallengeInfoMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeListMessage import (
    ChallengeListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeModSelectedMessage import (
    ChallengeModSelectedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeModSelectMessage import (
    ChallengeModSelectMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeNumberMessage import (
    ChallengeNumberMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeResultMessage import (
    ChallengeResultMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeSelectionMessage import (
    ChallengeSelectionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeTargetsListMessage import (
    ChallengeTargetsListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeTargetsListRequestMessage import (
    ChallengeTargetsListRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeTargetsMessage import (
    ChallengeTargetsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeTargetsRequestMessage import (
    ChallengeTargetsRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeTargetUpdateMessage import (
    ChallengeTargetUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.challenge.ChallengeValidateMessage import (
    ChallengeValidateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightEndMessage import GameFightEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightJoinMessage import (
    GameFightJoinMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightLeaveMessage import (
    GameFightLeaveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightResumeMessage import (
    GameFightResumeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightResumeWithSlavesMessage import (
    GameFightResumeWithSlavesMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightSpectateMessage import (
    GameFightSpectateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightSpectatorJoinMessage import (
    GameFightSpectatorJoinMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightStartingMessage import (
    GameFightStartingMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightStartMessage import (
    GameFightStartMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightUpdateTeamMessage import (
    GameFightUpdateTeamMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import (
    GameContextDestroyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextReadyMessage import (
    GameContextReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.CurrentMapInstanceMessage import (
    CurrentMapInstanceMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.CurrentMapMessage import CurrentMapMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapObstacleUpdateMessage import (
    MapObstacleUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultFighterListEntry import (
    FightResultFighterListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultListEntry import FightResultListEntry
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultPlayerListEntry import (
    FightResultPlayerListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightResultTaxCollectorListEntry import (
    FightResultTaxCollectorListEntry,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacterInformations import (
    GameFightCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEntityInformation import (
    GameFightEntityInformation,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterNamedInformations import (
    GameFightFighterNamedInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMutantInformations import (
    GameFightMutantInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightResumeSlaveInfo import (
    GameFightResumeSlaveInfo,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightTaxCollectorInformations import (
    GameFightTaxCollectorInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import (
    GameContextActorInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ClientStatusEnum import ClientStatusEnum


class FightContextFrame(Frame):

    FIGHT_RESULT_KEY_PREFIX: str = "fightResult_"

    MAX_FIGHT_RESULT: int = 15

    INVISIBLE_POSITION_SELECTION: str = "invisible_position"

    GLYPH_GFX_ID: str = "glyphGfxId"

    REACHABLE_CELL_COLOR: int = 26112

    UNREACHABLE_CELL_COLOR: int = 6684672

    def __init__(self):
        self.preFightIsActive: bool = True
        self._hiddenEntites = []
        self._fightersPositionsHistory = dict[int, list]()
        self._fightersRoundStartPosition = dict()
        self.onlyTheOtherTeamCanPlace: bool = False
        self.currentCell: int = -1
        self.fightResultId: float = 0
        self.fightResults: dict = dict()
        self.fightResultIds = list[str]()
        self._fightAttackerId: float = None
        self._fightType: int = None
        self._currentMapRenderId: int = -1
        self._entitiesFrame: FightEntitiesFrame
        self._preparationFrame: FightPreparationFrame
        self._battleFrame: FightBattleFrame
        self.isFightLeader = True
        self.fightLeader: GameContextActorInformations = None
        self._challengeSelectionMod = 1
        self._challengeBonusType = 0
        self._challengesList = list[ChallengeWrapper]()
        self.challengeChoicePhase = False
        super().__init__()

    def saveResults(self, resultsDescr: object) -> str:
        key: str = self.FIGHT_RESULT_KEY_PREFIX + str(self.fightResultId)
        self.fightResultId += 1
        self.fightResults[key] = resultsDescr
        self.fightResultIds.append(key)
        if len(self.fightResultIds) > self.MAX_FIGHT_RESULT:
            resultsToDeleteKey = self.fightResultIds.pop(0)
            if resultsToDeleteKey is not None and resultsToDeleteKey in self.fightResults:
                del self.fightResults[resultsToDeleteKey]
        return key

    def getResults(self, fightResultKey: str) -> object:
        if fightResultKey in self.fightResults:
            return self.fightResults[fightResultKey]
        return None

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def entitiesFrame(self) -> FightEntitiesFrame:
        return self._entitiesFrame

    @property
    def challengeMod(self):
        return self._challengeSelectionMod

    @property
    def challengeBonus(self):
        return self._challengeBonusType

    @property
    def challengesList(self):
        return self._challengesList

    @property
    def battleFrame(self) -> FightBattleFrame:
        return self._battleFrame

    @property
    def preparationFrame(self) -> FightPreparationFrame:
        return self._preparationFrame

    @property
    def fightType(self) -> int:
        return self._fightType

    @fightType.setter
    def fightType(self, t: int) -> None:
        self._fightType = t

    @property
    def isKolossium(self) -> bool:
        return self._fightType == FightTypeEnum.FIGHT_TYPE_PVP_ARENA

    @property
    def timelineOverEntity(self) -> bool:
        return self._timelineOverEntity

    @property
    def timelineOverEntityId(self) -> float:
        return self._timelineOverEntityId

    @property
    def hiddenEntities(self) -> list:
        return self._hiddenEntites

    @property
    def fightersPositionsHistory(self) -> dict:
        return self._fightersPositionsHistory

    def pushed(self) -> bool:
        InactivityManager().pause(True)
        self.currentCell = -1
        self._entitiesFrame = FightEntitiesFrame()
        self._preparationFrame = FightPreparationFrame(self)
        self._battleFrame = FightBattleFrame()
        Logger().debug("FightContextFrame pushed")
        return True

    def getFighterName(self, fighterId: float) -> str:
        fighterInfos = self.getFighterInfos(fighterId)
        if not fighterInfos:
            return "Unknown Fighter"

        if isinstance(fighterInfos, GameFightFighterNamedInformations):
            return fighterInfos.name

        if isinstance(fighterInfos, GameFightMonsterInformations):
            return Monster.getMonsterById(fighterInfos.creatureGenericId).name

        if isinstance(fighterInfos, GameFightEntityInformation):
            compInfos = fighterInfos
            genericName = Companion.getCompanionById(compInfos.entityModelId).name
            if compInfos.masterId != PlayedCharacterManager().id:
                masterName = self.getFighterName(compInfos.masterId)
                name = I18n.getUiText("ui.common.belonging", [genericName, masterName])
            else:
                name = genericName
            return name

        if isinstance(fighterInfos, GameFightTaxCollectorInformations):
            taxInfos = fighterInfos
            return (
                TaxCollectorFirstname.getTaxCollectorFirstnameById(taxInfos.firstNameId).firstname
                + " "
                + TaxCollectorName.getTaxCollectorNameById(taxInfos.lastNameId).name
            )

        else:
            return "Unknown Fighter Type"

    def getFighterLevel(self, fighterId: float) -> int:
        fighterInfos = self.getFighterInfos(fighterId)
        if not fighterInfos:
            return 0
        if isinstance(fighterInfos, GameFightMutantInformations):
            return fighterInfos.powerLevel

        if isinstance(fighterInfos, GameFightCharacterInformations):
            return fighterInfos.level

        if isinstance(fighterInfos, GameFightEntityInformation):
            return fighterInfos.level

        if isinstance(fighterInfos, GameFightMonsterInformations):
            if self.fightType == FightTypeEnum.FIGHT_TYPE_BREACH:
                minLevel = float("inf")
                for entity in self._entitiesFrame.entities.values():
                    if isinstance(entity, GameFightMonsterInformations):
                        creatureLevel = entity.creatureLevel
                    if fighterInfos.creatureGenericId == entity.creatureGenericId and entity.stats.summoned:
                        return creatureLevel
                    if not entity.stats.summoned:
                        if minLevel > creatureLevel:
                            minLevel = creatureLevel
                return minLevel
            if fighterInfos.stats.summoned:
                return self.getFighterLevel(fighterInfos.stats.summoner)
            return fighterInfos.creatureLevel
        if isinstance(fighterInfos, GameFightTaxCollectorInformations):
            return fighterInfos.level
        else:
            return 0

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightStartingMessage):
            gfsmsg = msg
            self.fightType = gfsmsg.fightType
            self._fightAttackerId = gfsmsg.attackerId
            PlayedCharacterManager().fightId = gfsmsg.fightId
            if PlayerManager().kisServerPort > 0:
                Logger().debug(
                    f"KIS fight started : {gfsmsg.fightId}-{PlayedCharacterManager().currentMap.mapId} (port : {PlayerManager().kisServerPort})"
                )
            else:
                Logger().debug(
                    f"Game fight started : {gfsmsg.fightId}-{PlayedCharacterManager().currentMap.mapId} (port : {PlayerManager().gameServerPort})"
                )
            CurrentPlayedFighterManager().currentFighterId = PlayedCharacterManager().id
            CurrentPlayedFighterManager().getSpellCastManager().currentTurn = 1
            return True

        elif isinstance(msg, CurrentMapMessage):
            mcmsg = msg
            Logger().info(f"Loading fight map {msg.mapId}...")
            if isinstance(mcmsg, CurrentMapInstanceMessage):
                mdm.MapDisplayManager().mapInstanceId = mcmsg.instantiatedMapId
            else:
                mdm.MapDisplayManager().mapInstanceId = 0
            wp = WorldPointWrapper(mcmsg.mapId)
            mdm.MapDisplayManager().loadMap(mcmsg.mapId)
            PlayedCharacterManager().currentMap = wp
            PlayedCharacterManager().currentSubArea = SubArea.getSubAreaByMapId(mcmsg.mapId)
            return True

        elif isinstance(msg, MapLoadedMessage):
            Logger().info(f"Fight Map Loaded")
            message = GameContextReadyMessage()
            message.init(int(mdm.MapDisplayManager().currentMapPoint.mapId))
            ConnectionsHandler().send(message)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.SWITCHED_TO_FIGHTING)
            return True

        elif isinstance(msg, GameFightResumeMessage):
            Logger().info(f"Fight resumed after disconnect")
            gfrmsg = msg
            playerId = PlayedCharacterManager().id
            CurrentPlayedFighterManager().setCurrentSummonedCreature(gfrmsg.summonCount, playerId)
            CurrentPlayedFighterManager().setCurrentSummonedBomb(gfrmsg.bombCount, playerId)
            self._battleFrame.turnsCount = gfrmsg.gameTurn
            if isinstance(msg, GameFightResumeWithSlavesMessage):
                gfrwsmsg = msg
                cooldownInfos = gfrwsmsg.slavesInfo
            else:
                cooldownInfos = list[GameFightResumeSlaveInfo]()
            playerCoolDownInfo = GameFightResumeSlaveInfo()
            playerCoolDownInfo.spellCooldowns = gfrmsg.spellCooldowns
            playerCoolDownInfo.slaveId = PlayedCharacterManager().id
            cooldownInfos.insert(0, playerCoolDownInfo)
            playedFighterManager = CurrentPlayedFighterManager()
            for cd in cooldownInfos:
                spellCastManager = playedFighterManager.getSpellCastManagerById(cd.slaveId)
                spellCastManager.currentTurn = gfrmsg.gameTurn
                spellCastManager.updateCooldowns(cd.spellCooldowns)
                if cd.slaveId != playerId:
                    playedFighterManager.setCurrentSummonedCreature(cd.summonCount, cd.slaveId)
                    playedFighterManager.setCurrentSummonedBomb(cd.bombCount, cd.slaveId)
            castingSpellPool = dict[int, dict[int, dict[int, SpellCastSequenceContext]]]()
            for buff in gfrmsg.effects:
                if not castingSpellPool.get(buff.effect.targetId):
                    castingSpellPool[buff.effect.targetId] = {}
                targetPool = castingSpellPool[buff.effect.targetId]
                if not targetPool.get(buff.effect.turnDuration):
                    targetPool[buff.effect.turnDuration] = {}
                durationPool = targetPool[buff.effect.turnDuration]
                castingSpell = durationPool.get(buff.effect.spellId)
                if not castingSpell:
                    castingSpell = SpellCastSequenceContext()
                    castingSpell.casterId = buff.sourceId
                    castingSpell.spellData = spellmod.Spell.getSpellById(buff.effect.spellId)
                    durationPool[buff.effect.spellId] = castingSpell
                buffTmp = BuffManager.makeBuffFromEffect(buff.effect, castingSpell, buff.actionId)
                BuffManager().addBuff(buffTmp)
            KernelEventsManager().send(KernelEvent.FightResumed)
            return True

        elif isinstance(msg, GameFightUpdateTeamMessage):
            gfutmsg = msg
            PlayedCharacterManager().teamId = gfutmsg.team.teamId
            return True

        elif isinstance(msg, GameFightSpectateMessage):
            return True

        elif isinstance(msg, GameFightSpectatorJoinMessage):
            return True

        elif isinstance(msg, GameFightJoinMessage):
            preFightIsActive = not msg.isFightStarted
            self.fightType = msg.fightType
            Kernel().worker.addFrame(self._entitiesFrame)
            if preFightIsActive:
                Kernel().worker.addFrame(self._preparationFrame)
                self.onlyTheOtherTeamCanPlace = not msg.isTeamPhase
            else:
                Kernel().worker.removeFrame(self._preparationFrame)
                Kernel().worker.addFrame(self._battleFrame)
                self.onlyTheOtherTeamCanPlace = False
            PlayedCharacterManager().isSpectator = False
            PlayedCharacterManager().isFighting = True
            timeBeforeStart = msg.timeMaxBeforeFightStart * 100
            if timeBeforeStart == 0 and preFightIsActive:
                timeBeforeStart = -1
            Logger().separator("Joined fight", "*")
            KernelEventsManager().send(
                KernelEvent.FightJoined,
                msg.isFightStarted,
                msg.fightType,
                msg.isTeamPhase,
                msg.timeMaxBeforeFightStart,
            )
            return True

        elif isinstance(msg, GameFightStartMessage):
            preFightIsActive = False
            Kernel().worker.removeFrame(self._preparationFrame)
            CurrentPlayedFighterManager().getSpellCastManager().resetInitialCooldown()
            Kernel().worker.addFrame(self._battleFrame)
            return True

        elif isinstance(msg, GameContextDestroyMessage):
            Kernel().worker.removeFrame(self)
            return False

        elif isinstance(msg, GameFightLeaveMessage):
            return False

        elif isinstance(msg, GameFightEndMessage):
            CurrentPlayedFighterManager().resetPlayerSpellList()
            PlayedCharacterManager().isFighting = False
            PlayedCharacterManager().fightId = -1
            SpellWrapper.removeAllSpellWrapperBut(PlayedCharacterManager().id, None)
            SpellWrapper.resetAllCoolDown(PlayedCharacterManager().id, None)
            SpellModifiersManager.clear()
            Kernel().worker.removeFrame(self)
            return False

        elif isinstance(msg, ChallengeTargetsListRequestAction):
            ctlra = msg
            ctlrmsg = ChallengeTargetsListRequestMessage()
            ctlrmsg.init(ctlra.challengeId)
            ConnectionsHandler().send(ctlrmsg)
            return True

        elif isinstance(msg, ChallengeTargetsListMessage):
            return True

        elif isinstance(msg, ChallengeInfoMessage):
            return True

        elif isinstance(msg, ChallengeTargetUpdateMessage):
            return True

        elif isinstance(msg, ChallengeResultMessage):
            return True

        elif isinstance(msg, ArenaFighterLeaveMessage):
            return True

        elif isinstance(msg, MapObstacleUpdateMessage):
            moumsg = msg
            for mo in moumsg.obstacles:
                DataMapProvider().updateCellMovLov(mo.obstacleCellId, mo.state == MapObstacleStateEnum.OBSTACLE_OPENED)
            return True

        elif isinstance(msg, GameActionFightNoSpellCastMessage):
            return False

        elif isinstance(msg, UpdateSpellModifierAction):
            usma = msg
            spellWrapper = SpellWrapper.getSpellWrapperById(usma.spellId, usma.entityId)
            if spellWrapper is not None:
                spellWrapper.versionNum += 1
                if usma.statId == CharacterSpellModificationTypeEnum.CAST_INTERVAL:
                    spellManager = (
                        CurrentPlayedFighterManager()
                        .getSpellCastManagerById(usma.entityId)
                        .getSpellManagerBySpellId(usma.spellId)
                    )
                    if spellManager is not None:
                        spellWrapper.actualCooldown = spellManager.cooldown
                elif usma.statId == CharacterSpellModificationTypeEnum.AP_COST:
                    pass
            return True

        elif isinstance(msg, ArenaFighterIdleMessage):
            return True

        if isinstance(msg, ChallengeNumberMessage):
            self._challengesList = [EmptyChallengeWrapper() for _ in range(msg.challengeNumber)]
            KernelEventsManager().send(KernelEvent.ChallengeListUpdate, self._challengesList)
            self.challengeBonusSelectAction(ChallengeBonusEnum.CHALLENGE_EXPERIENCE_BONUS)
            self.challengeModSelectAction(ChallengeModEnum.CHALLENGE_RANDOM)
            return True

        elif isinstance(msg, ChallengeListMessage):
            for chall in msg.challengesInformation:
                if Challenge.getChallengeById(chall.challengeId):
                    challengeW = self.getChallengeById(chall.challengeId)
                    if not challengeW:
                        challengeW = ChallengeWrapper()
                        self._challengesList.append(challengeW)
                    challengeW.id = chall.challengeId
                    challengeW.setTargetsFromTargetInformation(chall.targetsList)
                    challengeW.xpBonus = chall.xpBonus
                    challengeW.dropBonus = chall.dropBonus
                    challengeW.state = chall.state
            KernelEventsManager().send(KernelEvent.ChallengeListUpdate, self._challengesList)
            KernelEventsManager().send(KernelEvent.CloseChallengeProposal)
            return True

        elif isinstance(msg, ChallengeAddMessage):
            challInfo = msg.challengeInformation
            if not Challenge.getChallengeById(challInfo.challengeId):
                return True
            addedChall = self.getChallengeById(challInfo.challengeId)
            if not addedChall:
                addedChall = ChallengeWrapper()
                replaced = False
                for index, challenge in enumerate(self._challengesList):
                    if isinstance(challenge, EmptyChallengeWrapper):
                        self._challengesList[index] = addedChall
                        replaced = True
                        break
                if not replaced:
                    self._challengesList.append(addedChall)
            addedChall.id = challInfo.challengeId
            addedChall.setTargetsFromTargetInformation(challInfo.targetsList)
            addedChall.xpBonus = challInfo.xpBonus
            addedChall.dropBonus = challInfo.dropBonus
            addedChall.state = challInfo.state
            KernelEventsManager().send(KernelEvent.ChallengeListUpdate, self._challengesList)
            return True

        elif isinstance(msg, ChallengeTargetsMessage):
            challenge = self.getChallengeById(msg.challengeInformation.challengeId)
            if challenge is None:
                Logger().warn(
                    f"Got a challenge update with no corresponding challenge (challenge id {msg.challengeInformation.challengeId}), skipping."
                )
                return False
            challenge.setTargetsFromTargetInformation(msg.challengeInformation.targetsList)
            challenge.xpBonus = msg.challengeInformation.xpBonus
            challenge.dropBonus = msg.challengeInformation.dropBonus
            challenge.state = msg.challengeInformation.state
            for targetW in challenge.targets:
                if targetW.targetCell != -1 and (
                    PlayedCharacterManager().id in targetW.attackers or not targetW.attackers
                ):
                    Logger().debug(f"Showing challenge cell {targetW.targetCell}")
            return True

        if isinstance(msg, ChallengeResultMessage):
            challenge = self.getChallengeById(msg.challengeId)
            if not challenge:
                Logger().warning(
                    f"Got a challenge result with no corresponding challenge (challenge id {msg.challengeId}), skipping."
                )
                return False
            challenge.state = (
                ChallengeStateEnum.CHALLENGE_COMPLETED if msg.success else ChallengeStateEnum.CHALLENGE_FAILED
            )
            KernelEventsManager().send(KernelEvent.ChallengeListUpdate, self._challengesList)
            return True

        elif isinstance(msg, ChallengeModSelectedMessage):
            self._challengeSelectionMod = msg.challengeMod
            KernelEventsManager().send(KernelEvent.ChallengeModSelected, self._challengeSelectionMod)
            return True

        elif isinstance(msg, ChallengeBonusChoiceSelectedMessage):
            self._challengeBonusType = msg.challengeBonus
            KernelEventsManager().send(KernelEvent.ChallengeBonusSelected, self._challengeBonusType)
            return True

        return False

    def challengeTargetsRequestAction(self, challengeId):
        ctrmsg = ChallengeTargetsRequestMessage()
        ctrmsg.init(challengeId)
        ConnectionsHandler().send(ctrmsg)
        return True

    def challengeModSelectAction(self, mod):
        cmsmsg = ChallengeModSelectMessage()
        self._challengeSelectionMod = mod
        cmsmsg.init(mod)
        ConnectionsHandler().send(cmsmsg)
        return True

    def challengeBonusSelectAction(self, bonus):
        cbcmsg = ChallengeBonusChoiceMessage()
        cbcmsg.init(bonus)
        ConnectionsHandler().send(cbcmsg)
        return True

    def challengeSelectionAction(self, challengeId):
        csmsg = ChallengeSelectionMessage()
        csmsg.init(challengeId)
        ConnectionsHandler().send(csmsg)
        return True

    def challengeValidateAction(self, challengeId):
        cvmsg = ChallengeValidateMessage()
        cvmsg.init(challengeId)
        ConnectionsHandler().send(cvmsg)
        return True

    def getChallengeById(self, challengeId: int) -> ChallengeWrapper:
        challenge: ChallengeWrapper = None
        for challenge in self._challengesList:
            if challenge.id == challengeId:
                return challenge
        return None

    def pulled(self) -> bool:
        self._fightersRoundStartPosition.clear()
        self._fightersPositionsHistory.clear()
        if self._battleFrame:
            Kernel().worker.removeFrame(self._battleFrame)
        if self._entitiesFrame:
            Kernel().worker.removeFrame(self._entitiesFrame)
        if self._preparationFrame:
            Kernel().worker.removeFrame(self._preparationFrame)
        simf = Kernel().spellInventoryManagementFrame
        if simf:
            simf.deleteSpellsGlobalCoolDownsData()
        PlayedCharacterManager().isSpectator = False
        EntitiesManager().clearEntities()
        InactivityManager().pause(False)
        Logger().debug("FightContextFrame pulled")
        return True

    def addToHiddenEntities(self, entityId: float) -> None:
        if entityId not in self._hiddenEntites:
            self._hiddenEntites.append(entityId)

    def removeFromHiddenEntities(self, entityId: float) -> None:
        if entityId in self._hiddenEntites:
            self._hiddenEntites.remove(entityId)

    def initFighterPositionHistory(self, pFighterId: float) -> None:
        if pFighterId not in self._fightersPositionsHistory:
            self._fightersPositionsHistory[pFighterId] = [
                {
                    "cellId": self.entitiesFrame.getEntityInfos(pFighterId).disposition.cellId,
                    "lives": 2,
                }
            ]

    def getFighterPreviousPosition(self, pFighterId: float) -> int:
        self.initFighterPositionHistory(pFighterId)
        positions: list = self._fightersPositionsHistory[pFighterId]
        savedPos: object = positions[len(positions) - 2] if len(positions) > 1 else None
        return int(savedPos["cellId"] if savedPos else -1)

    def deleteFighterPreviousPosition(self, pFighterId: float) -> None:
        if self._fightersPositionsHistory[pFighterId]:
            self._fightersPositionsHistory[pFighterId].pop()

    def saveFighterPosition(self, pFighterId: float, pCellId: int) -> None:
        self.initFighterPositionHistory(pFighterId)
        self._fightersPositionsHistory[pFighterId].append({"cellId": pCellId, "lives": 2})

    def getFighterRoundStartPosition(self, pFighterId: float) -> int:
        return self._fightersRoundStartPosition[pFighterId]

    def setFighterRoundStartPosition(self, pFighterId: float, cellId: int) -> int:
        self._fightersRoundStartPosition[pFighterId] = cellId
        return cellId

    def getFighterInfos(self, fighterId: float) -> GameFightFighterInformations:
        return self.entitiesFrame.getEntityInfos(fighterId)

    def stopReconnection(self, *args) -> None:
        Kernel().beingInReconnection = False

    def buildFighResul(self, gfemsg: GameFightEndMessage) -> None:
        fightEnding = FightEndingMessage()
        fightEnding.init()
        Kernel().worker.process(fightEnding)
        results = list[FightResultEntryWrapper](len(gfemsg.results) * [None])
        resultIndex = 0
        winners = list[FightResultEntryWrapper]()
        temp = []
        for resultEntry in gfemsg.results:
            temp.append(resultEntry)
        isSpectator = True
        for i in range(len(temp)):
            resultEntry = temp[i]
            if isinstance(resultEntry, FightResultPlayerListEntry):
                id = resultEntry.id
                frew = FightResultEntryWrapper(resultEntry, self._entitiesFrame.getEntityInfos(id))
                frew.alive = resultEntry.alive
            if isinstance(resultEntry, FightResultTaxCollectorListEntry):
                id = resultEntry.id
                frew = FightResultEntryWrapper(
                    resultEntry,
                    self._entitiesFrame.getEntityInfos(id),
                )
                frew.alive = resultEntry.alive
            if isinstance(resultEntry, FightResultFighterListEntry):
                id = resultEntry.id
                frew = FightResultEntryWrapper(
                    resultEntry,
                    self._entitiesFrame.getEntityInfos(id),
                )
                frew.alive = resultEntry.alive

            if isinstance(resultEntry, FightResultListEntry):
                frew = FightResultEntryWrapper(resultEntry, None, isSpectator)

            frew.fightInitiator = self._fightAttackerId == id
            frew.wave = resultEntry.wave
            if (
                i + 1 < len(temp)
                and temp[i + 1]
                and temp[i + 1].outcome == resultEntry.outcome
                and temp[i + 1].wave != resultEntry.wave
            ):
                frew.isLastOfHisWave = True
            if resultEntry.outcome == FightOutcomeEnum.RESULT_DEFENDER_GROUP:
                hardcoreLoots = frew
            else:
                if resultEntry.outcome == FightOutcomeEnum.RESULT_VICTORY:
                    winners.append(frew)
                results[resultIndex] = frew
                resultIndex += 1
                if frew.id == CurrentPlayedFighterManager().currentFighterId:
                    isSpectator = False

        if hardcoreLoots:
            currentWinner = 0
            for loot in hardcoreLoots.rewards.objects:
                winners[currentWinner].rewards.objects.append(loot)
                currentWinner += 1
                currentWinner %= len(winners)
            kamas = hardcoreLoots.rewards.kamas
            kamasPerWinner = math.floor(kamas / len(winners))
            if kamas % len(winners) != 0:
                kamasPerWinner += 1
            for winner in winners:
                if kamas < kamasPerWinner:
                    winner.rewards.kamas = kamas
                else:
                    winner.rewards.kamas = kamasPerWinner
                kamas -= winner.rewards.kamas
        winnersName = ""
        losersName = ""
        for namedTeamWO in gfemsg.namedPartyTeamsOutcomes:
            if namedTeamWO.team.partyName and namedTeamWO.team.partyName != "":
                if namedTeamWO.outcome == FightOutcomeEnum.RESULT_VICTORY:
                    winnersName = namedTeamWO.team.partyName
                elif namedTeamWO.outcome == FightOutcomeEnum.RESULT_LOST:
                    losersName = namedTeamWO.team.partyName
        resultsRecap = {
            "results": results,
            "rewardRate": gfemsg.rewardRate,
            "sizeMalus": gfemsg.lootShareLimitMalus,
            "duration": gfemsg.duration,
            "challenges": self.challengesList,
            "turns": self._battleFrame.turnsCount,
            "fightType": self._fightType,
            "winnersName": winnersName,
            "losersName": losersName,
            "isSpectator": isSpectator,
        }
        if isinstance(gfemsg, BreachGameFightEndMessage):
            resultsRecap["budget"] = gfemsg.budget
        return resultsRecap
