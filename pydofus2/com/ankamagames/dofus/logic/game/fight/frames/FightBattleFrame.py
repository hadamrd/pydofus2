from time import sleep
from types import FunctionType
from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper as spellwrapper
import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
import pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame as pcuF
import pydofus2.com.ankamagames.dofus.logic.game.fight.fightEvents.FightEventsHelper as fevth
import pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame as fenf
import pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSequenceFrame as fseqf
import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager as bffm
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SpellInventoryManagementFrame import SpellInventoryManagementFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightTurnFinishAction import GameFightTurnFinishAction
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSequenceSwitcherFrame import FightSequenceSwitcherFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import FightTurnFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import FightersStateManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellCastInFightManager import SpellCastInFightManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import FightEntitiesHolder
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import StatBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.TriggeredBuff import TriggeredBuff
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDeathMessage import (
    GameActionFightDeathMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionUpdateEffectTriggerCountMessage import (
    GameActionUpdateEffectTriggerCountMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.GameActionAcknowledgementMessage import (
    GameActionAcknowledgementMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceEndMessage import SequenceEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceStartMessage import SequenceStartMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.CharacterStatsListMessage import (
    CharacterStatsListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.UpdateSpellModifierMessage import (
    UpdateSpellModifierMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightEndMessage import GameFightEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightLeaveMessage import GameFightLeaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightNewRoundMessage import GameFightNewRoundMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightNewWaveMessage import GameFightNewWaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPauseMessage import GameFightPauseMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightSynchronizeMessage import (
    GameFightSynchronizeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnEndMessage import GameFightTurnEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnListMessage import GameFightTurnListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnReadyMessage import (
    GameFightTurnReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnReadyRequestMessage import (
    GameFightTurnReadyRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnResumeMessage import (
    GameFightTurnResumeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnStartMessage import (
    GameFightTurnStartMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.SlaveNoLongerControledMessage import (
    SlaveNoLongerControledMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.SlaveSwitchContextMessage import (
    SlaveSwitchContextMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import GameContextDestroyMessage
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacterInformations import (
    GameFightCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import FightContextFrame

logger = Logger("Dofus2")


class FightBattleFrame(Frame):

    FIGHT_SEQUENCER_NAME: str = "FightBattleSequencer"

    isFightAboutToEnd: bool = False

    _sequenceFrameSwitcher: FightSequenceSwitcherFrame = None

    _turnFrame: FightTurnFrame = None

    _currentSequenceFrame: fseqf.FightSequenceFrame = None

    _sequenceFrames: list[fseqf.FightSequenceFrame] = []

    _executingSequence: bool = False

    _confirmTurnEnd: bool = None

    _endBattle: bool = False

    _battleResults: GameFightEndMessage = None

    _refreshTurnsList: bool = None

    _newTurnsList: list[float] = None

    _newDeadTurnsList: list[float] = []

    _turnsList: list[float] = None

    _deadTurnsList: list[float] = []

    _playerTargetedEntitiesList: list[float] = None

    _fightIsPaused: bool = False

    _deathPlayingNumber: int = 0

    _synchroniseFighters: list[GameFightFighterInformations] = None

    _synchroniseFightersInstanceId: int = 4.294967295e9

    _neverSynchronizedBefore: bool = True

    _delayCslmsg: CharacterStatsListMessage = None

    _playerNewTurn: AnimatedCharacter = None

    _turnsCount: int = 0

    _destroyed: bool = False

    _playingSlaveEntity: bool = False

    _lastPlayerId: float = None

    _nextLastPlayerId: float = None

    _currentPlayerId: float = None

    _skipTurnTimer: BenchmarkTimer = None

    _masterId: float = None

    _slaveId: float = None

    _autoEndTurn: bool = False

    _newWave: bool = False

    _newWaveId: int = 0

    _sequenceFrameCached: fseqf.FightSequenceFrame = None

    def __init__(self):
        self._playerTargetedEntitiesList = list[float]()
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def fightIsPaused(self) -> bool:
        return self._fightIsPaused

    @property
    def fightersList(self) -> list[float]:
        return self._turnsList

    @fightersList.setter
    def fightersList(self, turnList: list[float]) -> None:
        self._turnsList = turnList

    @property
    def deadFightersList(self) -> list[float]:
        return self._deadTurnsList

    @deadFightersList.setter
    def deadFightersList(self, deadTurnList: list[float]) -> None:
        self._deadTurnsList = deadTurnList

    @property
    def targetedEntities(self) -> list[float]:
        return self._playerTargetedEntitiesList

    @property
    def turnsCount(self) -> int:
        return self._turnsCount

    @turnsCount.setter
    def turnsCount(self, turn: int) -> None:
        self._turnsCount = turn

    @property
    def currentPlayerId(self) -> float:
        if self._currentPlayerId is None:
            return PlayedCharacterManager().id
        return self._currentPlayerId

    @property
    def executingSequence(self) -> bool:
        return self._executingSequence

    @property
    def currentSequenceFrame(self) -> fseqf.FightSequenceFrame:
        return self._currentSequenceFrame

    @property
    def playingSlaveEntity(self) -> bool:
        return self._playingSlaveEntity

    @property
    def slaveId(self) -> float:
        return self._slaveId

    @property
    def masterId(self) -> float:
        return self._masterId

    @property
    def deathPlayingNumber(self) -> int:
        return self._deathPlayingNumber

    @deathPlayingNumber.setter
    def deathPlayingNumber(self, n: int) -> None:
        self._deathPlayingNumber = n

    def pushed(self) -> bool:
        self._turnFrame = FightTurnFrame()
        self._playingSlaveEntity = False
        self._sequenceFrames = []
        DataMapProvider().isInFight = True
        logger.debug(f"FightBattleFrame pushed, dataMapProvider.isInFight = {DataMapProvider().isInFight}")
        krnl.Kernel().worker.addFrame(self._turnFrame)
        self._destroyed = False
        self._neverSynchronizedBefore = True
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightTurnListMessage):
            gftmsg = msg
            if self._executingSequence or self._currentSequenceFrame:
                logger.warn(
                    "There was a turns list update during self sequence... Let's wait its finish before doing it."
                )
                self._refreshTurnsList = True
                self._newTurnsList = gftmsg.ids
                self._newDeadTurnsList = gftmsg.deadsIds
            else:
                self.updateTurnsList(gftmsg.ids, gftmsg.deadsIds)
            return True

        elif isinstance(msg, GameFightSynchronizeMessage):
            gftcimsg = msg
            if self._newWave:
                for fighter in gftcimsg.fighters:
                    if (
                        fighter.spawnInfo.alive
                        and fighter.wave == self._newWaveId
                        and not fenf.FightEntitiesFrame.getCurrentInstance().getEntityInfos(fighter.contextualId)
                    ):
                        fenf.FightEntitiesFrame.getCurrentInstance().addOrUpdateActor(fighter)
            if self._executingSequence:
                self._synchroniseFighters = gftcimsg.fighters
                self._synchroniseFightersInstanceId = fseqf.FightSequenceFrame.currentInstanceId
            else:
                self.gameFightSynchronize(gftcimsg.fighters)
            return False

        elif isinstance(msg, GameActionUpdateEffectTriggerCountMessage):
            gauetcmsg = msg
            for effectTrigger in gauetcmsg.targetIds:
                for buffTriggered in bffm.BuffManager().getAllBuff(effectTrigger.targetId):
                    if (
                        isinstance(buffTriggered, TriggeredBuff)
                        and buffTriggered.effect.effectUid == effectTrigger.effectId
                    ):
                        buffTriggered.triggerCount = effectTrigger.count
            return True

        elif isinstance(msg, SlaveSwitchContextMessage):
            sscmsg = msg
            playerId = PlayedCharacterManager().id
            if sscmsg.masterId == playerId:
                self._masterId = sscmsg.masterId
                self._slaveId = sscmsg.slaveId
                if not self._currentPlayerId and self._turnsList.index(self._masterId) > self._turnsList.index(
                    self._slaveId
                ):
                    self.prepareNextPlayableCharacter(self._masterId)
            return False

        elif isinstance(msg, SlaveNoLongerControledMessage):
            snlcmsg = msg
            playerId = PlayedCharacterManager().id
            if snlcmsg.masterId != playerId and self._slaveId == snlcmsg.slaveId:
                self._masterId = playerId
                self._slaveId = self._masterId
                self.prepareNextPlayableCharacter(playerId)
                self._slaveId = 0
            return False

        elif isinstance(msg, GameFightTurnStartMessage):
            fightEntitesFrame: "fenf.FightEntitiesFrame" = krnl.Kernel().worker.getFrame("FightEntitiesFrame")
            gftsmsg = msg
            playerId = PlayedCharacterManager().id
            self._currentPlayerId = gftsmsg.id
            if not self._lastPlayerId:
                self._lastPlayerId = self._currentPlayerId
            # logger.info("*" * 50 + f"   Start turn for entityId {self._currentPlayerId}    " + "*" * 50)
            if self._currentPlayerId == playerId:
                self._slaveId = 0
            self._playingSlaveEntity = gftsmsg.id == self._slaveId
            # logger.debug("Playing slave entity: " + str(self._playingSlaveEntity))
            self._turnFrame.turnDuration = gftsmsg.waitTime * 0.1
            isResumeMessage = isinstance(msg, GameFightTurnResumeMessage)
            if not isResumeMessage:
                bffm.BuffManager().decrementDuration(gftsmsg.id)
                bffm.BuffManager().resetTriggerCount(gftsmsg.id)
            else:
                currentPlayedFighterId = CurrentPlayedFighterManager().currentFighterId
                nextPlayable = self.getNextPlayableCharacterId()
                if (
                    self._slaveId
                    and self._currentPlayerId != currentPlayedFighterId
                    and (self._slaveId == self._currentPlayerId or nextPlayable == self._slaveId)
                ):
                    logger.debug(f"Slave {self._slaveId} is now controlling the fight.")
                    self.prepareNextPlayableCharacter(self._masterId)
            if gftsmsg.id > 0 or self._playingSlaveEntity:
                entityInfo = fightEntitesFrame.getEntityInfos(gftsmsg.id)
                if (
                    entityInfo
                    and entityInfo.disposition.cellId != -1
                    and not FightEntitiesHolder().getEntity(gftsmsg.id)
                ):
                    entity: AnimatedCharacter = DofusEntities.getEntity(gftsmsg.id)
                    self._playerNewTurn = entity
            deadEntityInfo: GameFightFighterInformations = fightEntitesFrame.getEntityInfos(gftsmsg.id)
            if (
                (gftsmsg.id == playerId or self._playingSlaveEntity)
                and deadEntityInfo
                and deadEntityInfo.spawnInfo.alive
            ):
                CurrentPlayedFighterManager().currentFighterId = gftsmsg.id
                spellwrapper.SpellWrapper.refreshAllPlayerSpellHolder(gftsmsg.id)
                # logger.debug("Finaly turn for entityId: " + str(self._currentPlayerId) + " set to true")
                self._turnFrame.myTurn = True
            else:
                self._turnFrame.myTurn = False
            if self._skipTurnTimer:
                self._skipTurnTimer.cancel()
            if gftsmsg.id == playerId or self._playingSlaveEntity:
                alivePlayers = 0
                for en in fightEntitesFrame.entities.values():
                    if isinstance(en, GameFightCharacterInformations) and en.spawnInfo.alive and en.contextualId > 0:
                        alivePlayers += 1
            self.removeSavedPosition(gftsmsg.id)
            entitiesIds = fightEntitesFrame.getEntitiesIdsList()
            for entityId in entitiesIds:
                fighterInfos: "GameFightFighterInformations" = fightEntitesFrame.getEntityInfos(entityId)
                if fighterInfos and fighterInfos.stats.summoner == gftsmsg.id:
                    self.removeSavedPosition(entityId)
            krnl.Kernel().worker.getFrame("FightContextFrame")
            return False

        elif isinstance(msg, GameFightTurnEndMessage):
            gftemsg = msg
            if not self._confirmTurnEnd:
                self._lastPlayerId = gftemsg.id
            else:
                self._nextLastPlayerId = gftemsg.id
            entityInfos = fenf.FightEntitiesFrame.getCurrentInstance().getEntityInfos(gftemsg.id)
            if isinstance(entityInfos, GameFightFighterInformations) and not entityInfos:
                bffm.BuffManager().markFinishingBuffs(gftemsg.id)
                if gftemsg.id == CurrentPlayedFighterManager().currentFighterId:
                    CurrentPlayedFighterManager().getSpellCastManager().nextTurn()
                    spellwrapper.SpellWrapper.refreshAllPlayerSpellHolder(gftemsg.id)
            if gftemsg.id == CurrentPlayedFighterManager().currentFighterId:
                self._turnFrame.myTurn = False
            return True

        elif isinstance(msg, SequenceStartMessage):
            # logger.debug(f"[SEQ DEBUG] =================>> Received Sequence start author {msg.authorId}")
            self._autoEndTurn = False
            if not self._sequenceFrameSwitcher:
                # logger.debug(f"[SEQ DEBUG] Switcher is not set, creating new one")
                self._sequenceFrameSwitcher = FightSequenceSwitcherFrame()
                krnl.Kernel().worker.addFrame(self._sequenceFrameSwitcher)
            self._currentSequenceFrame = fseqf.FightSequenceFrame(self, self._currentSequenceFrame)
            self._sequenceFrameSwitcher.currentFrame = self._currentSequenceFrame
            return False

        elif isinstance(msg, SequenceEndMessage):
            # self.logState()
            semsg = msg
            if not self._currentSequenceFrame:
                logger.warn("Wow wow wow, I've got a Sequence End but no Sequence Start? What the hell?")
                return True
            self._currentSequenceFrame.mustAck = semsg.authorId == int(CurrentPlayedFighterManager().currentFighterId)
            self._currentSequenceFrame.ackIdent = semsg.actionId
            self._sequenceFrameSwitcher.currentFrame = None
            # logger.debug(
            #     f"================>> Received sequence #{self._currentSequenceFrame._instanceId} end with id: {semsg.actionId} and author id: {semsg.authorId}"
            # )
            if not self._currentSequenceFrame.parent:
                # logger.debug(
                #     f"Sequence {self._currentSequenceFrame._instanceId} is root, removing it and executing next sequence"
                # )
                krnl.Kernel().worker.removeFrame(self._sequenceFrameSwitcher)
                self._sequenceFrameSwitcher = None
                self._sequenceFrames.append(self._currentSequenceFrame)
                self._currentSequenceFrame = None
                self.executeNextSequence()
            else:
                # logger.debug(
                #     f"Sequence #{self._currentSequenceFrame._instanceId} is not the last one, so we will wait for the end of the parent sequence"
                # )
                self._currentSequenceFrame.execute()
                self._sequenceFrameSwitcher.currentFrame = self._currentSequenceFrame.parent
                self._currentSequenceFrame = self._currentSequenceFrame.parent
            return False

        elif isinstance(msg, GameFightTurnReadyRequestMessage):
            self.confirmTurnEnd()
            return False

        elif isinstance(msg, GameFightNewWaveMessage):
            gfnwmsg = msg
            self._newWaveId = gfnwmsg.id
            self._newWave = True
            return True

        elif isinstance(msg, GameFightNewRoundMessage):
            gfnrmsg = msg
            self._turnsCount = gfnrmsg.roundNumber
            CurrentPlayedFighterManager().getSpellCastManager().currentTurn = self._turnsCount
            logger.debug(f"[BUFFS DEBUG] Fight turn {self._turnsCount} started!")
            bffm.BuffManager().spellBuffsToIgnore = []
            return True

        elif isinstance(msg, GameFightLeaveMessage):
            gflmsg = msg
            fighterInfos2 = fenf.FightEntitiesFrame.getCurrentInstance().getEntityInfos(self._lastPlayerId)
            leaveSequenceFrame = fseqf.FightSequenceFrame(self)
            if fighterInfos2 and fighterInfos2.spawnInfo.alive:
                fakeDeathMessage = GameActionFightDeathMessage()
                leaveSequenceFrame.process(fakeDeathMessage.init(0, 0, gflmsg.charId))
                self._sequenceFrames.append(leaveSequenceFrame)
                self.executeNextSequence()
            return True

        elif isinstance(msg, GameFightEndMessage):
            gfemsg = msg
            maxEndRescue = 5
            maxEndRescue -= 1
            self.endBattle(gfemsg)
            FightersStateManager().endFight()
            CurrentPlayedFighterManager().endFight()
            return False

        elif isinstance(msg, GameContextDestroyMessage):
            if self._battleResults:
                logger.debug("Fin de combat propre (resultat connu)")
                self.endBattle(self._battleResults)
            else:
                logger.debug("Fin de combat brutale (pas de resultat connu)")
                self._executingSequence = False
                fakegfemsg = GameFightEndMessage()
                fakegfemsg.init(0, 0, 0, None, [])
                self.process(fakegfemsg)
            return False

        elif isinstance(msg, GameFightPauseMessage):
            gfpmsg = msg
            if gfpmsg.isPaused:
                logger.debug("The fight is paused.")
            else:
                logger.debug("The fight is resuming after pause.")
            self._fightIsPaused = gfpmsg.isPaused
            return True

        elif isinstance(msg, UpdateSpellModifierMessage):
            usmmsg = msg
            SpellModifiersManager().setRawSpellModifier(usmmsg.actorId, usmmsg.spellModifier)
            return True

        else:
            return False

    def pulled(self) -> bool:
        fsf: fseqf.FightSequenceFrame = None
        self.applyDelayedStats()
        DataMapProvider().isInFight = False
        if krnl.Kernel().worker.contains("FightTurnFrame"):
            krnl.Kernel().worker.removeFrame(self._turnFrame)
        bffm.BuffManager.clear()
        if self._executingSequence or krnl.Kernel().worker.contains("FightSequenceFrame"):
            fsf = krnl.Kernel().worker.getFrame("FightSequenceFrame")
            krnl.Kernel().worker.removeFrame(fsf)
        self._currentSequenceFrame = None
        self._sequenceFrameSwitcher = None
        self._turnFrame = None
        self._battleResults = None
        self._newTurnsList = None
        self._newDeadTurnsList = None
        self._turnsList = None
        self._deadTurnsList = None
        self._sequenceFrames = None
        self._playingSlaveEntity = False
        self._masterId = 0
        self._slaveId = 0
        self._playerNewTurn = None
        self._skipTurnTimer = None
        self._destroyed = True
        return True

    def getSequencesStack(self) -> list[fseqf.FightSequenceFrame]:
        res = []
        seq = self._currentSequenceFrame
        while seq:
            res.insert(0, seq)
            seq = seq._parent
        return res

    def logState(self):
        logger.debug(
            "****************************************************************** Current Sequences state ***********************************************************"
        )
        logger.debug(f"Executing a sequence : {self._executingSequence}")
        logger.debug(
            f"Sequence cached : #{self._sequenceFrameCached._instanceId if self._sequenceFrameCached else 'None'}"
        )
        logger.debug(
            f"Sequence current : #{self._currentSequenceFrame._instanceId if self._currentSequenceFrame else 'None'}"
        )
        padd = ""
        res = self.getSequencesStack()
        for seq in res:
            logger.debug(f"{padd}|---> Sequence #{seq._instanceId}")
            for step in seq._stepsBuffer:
                logger.debug(f"{padd}\t|---> {step.__class__.__name__}")
            padd += "\t"
        logger.debug(
            "****************************************************************************************************************************************************************"
        )

    def delayCharacterStatsList(self, msg: CharacterStatsListMessage) -> None:
        self._delayCslmsg = msg

    def prepareNextPlayableCharacter(self, currentCharacterId: float = 0) -> None:
        nextCharacterEntity: GameFightFighterInformations = None
        nextCharacterId: float = None
        if self._slaveId:
            if currentCharacterId:
                nextCharacterId = (
                    float(self._masterId) if currentCharacterId == self._slaveId else float(self._slaveId)
                )
            else:
                nextCharacterId = self.getNextPlayableCharacterId()
            nextCharacterEntity = fenf.FightEntitiesFrame.getCurrentInstance().getEntityInfos(nextCharacterId)
            if not nextCharacterEntity or not nextCharacterEntity.spawnInfo.alive:
                return
            CurrentPlayedFighterManager().currentFighterId = nextCharacterId
            if nextCharacterId == self._masterId:
                # FightApi.slaveContext = False
                CurrentPlayedFighterManager().resetPlayerSpellList()
                SpellInventoryManagementFrame().applySpellGlobalCoolDownInfo(self._masterId)
            elif nextCharacterId == self._slaveId:
                pass

    def getNextPlayableCharacterId(self) -> float:
        masterIdx: int = 0
        slaveIdx: int = 0
        currentCharacterIdx: int = 0
        currentPlayedCharacterId: float = CurrentPlayedFighterManager().currentFighterId
        if not self._slaveId or not self._turnsList:
            return currentPlayedCharacterId
        for i in range(len(self._turnsList)):
            if self._turnsList[i] == self._masterId:
                masterIdx = i
            elif self._turnsList[i] == self._slaveId:
                slaveIdx = i
            if self._turnsList[i] == self._currentPlayerId:
                currentCharacterIdx = i
        if masterIdx == currentCharacterIdx:
            return self._slaveId
        if slaveIdx == currentCharacterIdx:
            return self._masterId
        if masterIdx < currentCharacterIdx and slaveIdx > currentCharacterIdx:
            return self._slaveId
        if masterIdx > currentCharacterIdx and slaveIdx < currentCharacterIdx:
            return self._masterId
        if masterIdx > slaveIdx and masterIdx < currentCharacterIdx:
            return self._slaveId
        if masterIdx < slaveIdx and masterIdx < currentCharacterIdx:
            return self._masterId
        if masterIdx > slaveIdx and masterIdx > currentCharacterIdx:
            return self._slaveId
        if masterIdx < slaveIdx and masterIdx > currentCharacterIdx:
            return self._masterId
        return 0

    def executeNextSequence(self) -> bool:
        if self._executingSequence:
            return False
        if self._sequenceFrames:
            nextSequenceFrame: fseqf.FightSequenceFrame = self._sequenceFrames.pop(0)
            # logger.debug(f"Executing next sequence #{nextSequenceFrame._instanceId}")
            self._executingSequence = True
            nextSequenceFrame.execute(self.finishSequence(nextSequenceFrame))
            return False
        return False

    def applyDelayedStats(self) -> None:
        if not self._delayCslmsg:
            return
        characterFrame: pcuF.PlayedCharacterUpdatesFrame = (
            krnl.Kernel().worker.getFrame("PlayedCharacterUpdatesFrame")
        )
        if characterFrame:
            characterFrame.updateCharacterStatsList(self._delayCslmsg.stats)
        self._delayCslmsg = None

    def onLastAnimationFinished(self, tiphonEvent=None) -> None:
        self.sendAcknowledgement()
        if self._confirmTurnEnd:
            self.confirmDelayedTurnEnd()

    def sendAcknowledgement(self) -> None:
        if self._sequenceFrameCached == None:
            return
        ack: GameActionAcknowledgementMessage = GameActionAcknowledgementMessage()
        # logger.debug(f"Sending acknowledgement for sequence #{self._sequenceFrameCached._instanceId}")
        ack.init(True, self._sequenceFrameCached.ackIdent)
        self._sequenceFrameCached = None
        try:
            ConnectionsHandler()._conn.send(ack)
        except Exception as e:
            pass

    def finishSequence(self, sequenceFrame: fseqf.FightSequenceFrame) -> FunctionType:
        def function() -> None:
            if self._destroyed:
                return
            if sequenceFrame.mustAck:
                self._sequenceFrameCached = sequenceFrame
                if not self.isFightAboutToEnd:
                    self.sendAcknowledgement()
            fevth.FightEventsHelper().sendAllFightEvent(True)
            self._executingSequence = False
            if self._refreshTurnsList:
                logger.warn("There was a turns list refresh delayed, what about updating it now?")
                self._refreshTurnsList = False
                self.updateTurnsList(self._newTurnsList, self._newDeadTurnsList)
                self._newTurnsList = None
                self._newDeadTurnsList = None
            if (
                not self._executingSequence
                and len(self._sequenceFrames)
                and self._sequenceFrames[0].instanceId >= self._synchroniseFightersInstanceId
            ):
                self.gameFightSynchronize(self._synchroniseFighters)
                self._synchroniseFighters = None
            if self.executeNextSequence():
                self.applyDelayedStats()
                return
            if self._synchroniseFighters:
                self.gameFightSynchronize(self._synchroniseFighters)
                self._synchroniseFighters = None
            self.applyDelayedStats()
            if self._endBattle:
                logger.warn("This fight must end ! Finishing things now.")
                self._endBattle = False
                self.endBattle(self._battleResults)
                self._battleResults = None
                return
            if self._confirmTurnEnd and not self.isFightAboutToEnd:
                self.confirmDelayedTurnEnd()

        return function

    def confirmDelayedTurnEnd(self) -> None:
        logger.warn("There was a turn end delayed, dispatching now.")
        self._confirmTurnEnd = False
        if self._nextLastPlayerId is not None:
            self._lastPlayerId = self._nextLastPlayerId
        self._nextLastPlayerId = None
        self.confirmTurnEnd()

    def sendAutoEndTurn(self, e) -> None:
        action: Action = None
        if self._autoEndTurn:
            action = GameFightTurnFinishAction()
            krnl.Kernel().worker.process(action)
            self._autoEndTurn = False

    def updateTurnsList(self, turnsList: list[float], deadTurnsList: list[float]) -> None:
        self._turnsList = turnsList
        self._deadTurnsList = deadTurnsList

    def confirmTurnEnd(self) -> None:
        fighterInfos: GameFightFighterInformations = fenf.FightEntitiesFrame.getCurrentInstance().getEntityInfos(
            self._lastPlayerId
        )
        if fighterInfos:
            bffm.BuffManager().markFinishingBuffs(self._lastPlayerId)
            if self._lastPlayerId == CurrentPlayedFighterManager().currentFighterId:
                spellwrapper.SpellWrapper.refreshAllPlayerSpellHolder(self._lastPlayerId)
                self._playerTargetedEntitiesList = []
                self.prepareNextPlayableCharacter(self._lastPlayerId)
        spellCastManager: SpellCastInFightManager = CurrentPlayedFighterManager().getSpellCastManagerById(
            self._lastPlayerId
        )
        if spellCastManager is not None:
            spellCastManager.nextTurn()
        turnEnd: GameFightTurnReadyMessage = GameFightTurnReadyMessage()
        turnEnd.init(True)
        ConnectionsHandler()._conn.send(turnEnd)
        # logger.debug("Turn end confirmed.")

    def endBattle(self, fightEnd: GameFightEndMessage) -> None:
        self._holder: FightEntitiesHolder = FightEntitiesHolder()
        self._holder.reset()
        self._synchroniseFighters = None
        krnl.Kernel().worker.removeFrame(self)
        fightContextFrame = krnl.Kernel().worker.getFrame("FightContextFrame")
        fightContextFrame.process(fightEnd)

    def onSkipTurnTimeOut(self, event) -> None:
        self._skipTurnTimer.cancel()

    def gameFightSynchronize(self, fighters: list[GameFightFighterInformations]) -> None:
        newWaveAppeared: bool = False
        newWaveMonster: bool = False
        entitiesFrame: fenf.FightEntitiesFrame = krnl.Kernel().worker.getFrame("FightEntitiesFrame")
        newWaveMonsterIndex: int = 0
        bffm.BuffManager().synchronize()
        for fighterInfos in fighters:
            if fighterInfos.spawnInfo.alive:
                newWaveMonster = (
                    fighterInfos.wave == self._newWaveId
                    and fighterInfos.wave != 0
                    and not DofusEntities.getEntity(fighterInfos.contextualId)
                )
                entitiesFrame.updateFighter(fighterInfos)
                bffm.BuffManager().markFinishingBuffs(fighterInfos.contextualId, False)
                for buff in bffm.BuffManager().getAllBuff(fighterInfos.contextualId):
                    if isinstance(buff, StatBuff):
                        buff.isRecent = False
                if newWaveMonster:
                    newWaveAppeared = True
                    DofusEntities.getEntity(fighterInfos.contextualId).visible = False
                    sleep(0.3 * newWaveMonsterIndex)
                    entity = DofusEntities.getEntity(self._fighterId)
                    if entity:
                        entity.visible = self._visibility
                    newWaveMonsterIndex += 1
        if newWaveAppeared:
            self._newWave = False
            self._newWaveId = -1
        if self._neverSynchronizedBefore:
            self._neverSynchronizedBefore = False

    def removeSavedPosition(self, pEntityId: float) -> None:
        fightContextFrame: "FightContextFrame" = krnl.Kernel().worker.getFrame("FightContextFrame")
        savedPositions: list = fightContextFrame.fightersPositionsHistory.get(pEntityId)
        if savedPositions:
            nbPos = len(savedPositions)
            i = 0
            while i < nbPos:
                savedPos = savedPositions[i]
                savedPos["lives"] -= 1
                if savedPos["lives"] == 0:
                    del savedPositions[i]
                    i -= 1
                    nbPos -= 1
                i += 1
