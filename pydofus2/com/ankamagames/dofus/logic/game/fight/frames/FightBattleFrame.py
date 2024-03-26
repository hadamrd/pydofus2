from types import FunctionType

import pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame as pcuF
import pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSequenceFrame as fseqf
import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.BuffManager as bffm
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import \
    DataMapProvider
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import \
    SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import \
    StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightTurnFinishAction import \
    GameFightTurnFinishAction
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSequenceSwitcherFrame import \
    FightSequenceSwitcherFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightTurnFrame import \
    FightTurnFrame
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
    CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import \
    FightersStateManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import \
    SpellModifiersManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import \
    FightEntitiesHolder
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.StatBuff import \
    StatBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.TriggeredBuff import \
    TriggeredBuff
from pydofus2.com.ankamagames.dofus.misc.utils.GameDebugManager import \
    GameDebugManager
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDeathMessage import \
    GameActionFightDeathMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionUpdateEffectTriggerCountMessage import \
    GameActionUpdateEffectTriggerCountMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.GameActionAcknowledgementMessage import \
    GameActionAcknowledgementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceEndMessage import \
    SequenceEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.sequence.SequenceStartMessage import \
    SequenceStartMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.spellmodifier.ApplySpellModifierMessage import \
    ApplySpellModifierMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.spellmodifier.RemoveSpellModifierMessage import \
    RemoveSpellModifierMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.stats.CharacterStatsListMessage import \
    CharacterStatsListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightEndMessage import \
    GameFightEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightLeaveMessage import \
    GameFightLeaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightNewRoundMessage import \
    GameFightNewRoundMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightNewWaveMessage import \
    GameFightNewWaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPauseMessage import \
    GameFightPauseMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightSynchronizeMessage import \
    GameFightSynchronizeMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnEndMessage import \
    GameFightTurnEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnListMessage import \
    GameFightTurnListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.SlaveNoLongerControledMessage import \
    SlaveNoLongerControledMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import \
    GameContextDestroyMessage
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class FightBattleFrame(Frame):

    FIGHT_SEQUENCER_NAME: str = "FightBattleSequencer"

    def __init__(self):
        self._sequenceFrameSwitcher: FightSequenceSwitcherFrame = None
        self._turnFrame: FightTurnFrame = None
        self._currentSequenceFrame: fseqf.FightSequenceFrame = None
        self._sequenceFrames: list[fseqf.FightSequenceFrame] = []
        self._executingSequence: bool = False
        self._confirmTurnEnd: bool = None
        self._battleResults: GameFightEndMessage = None
        self._refreshTurnsList: bool = None
        self._newTurnsList: list[float] = None
        self._newDeadTurnsList: list[float] = []
        self._turnsList: list[float] = None
        self.deadTurnsList: list[float] = []
        self._fightIsPaused: bool = False
        self._synchroniseFighters: list[GameFightFighterInformations] = None
        self._synchroniseFightersInstanceId: int = 4.294967295e9
        self._neverSynchronizedBefore: bool = True
        self._delayCslmsg: CharacterStatsListMessage = None
        self._turnsCount: int = 0
        self._destroyed: bool = False
        self._lastPlayerId: float = None
        self._nextLastPlayerId: float = None
        self._masterId: float = None
        self._slaveId: float = None
        self._autoEndTurn: bool = False
        self._newWaveId: int = 0
        self._newWave = False
        self._sequenceFrameCached: fseqf.FightSequenceFrame = None
        self._endBattle = False
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
        return self.deadTurnsList

    @deadFightersList.setter
    def deadFightersList(self, deadTurnList: list[float]) -> None:
        self.deadTurnsList = deadTurnList

    @property
    def turnsCount(self) -> int:
        return self._turnsCount

    @turnsCount.setter
    def turnsCount(self, turn: int) -> None:
        self._turnsCount = turn

    @property
    def executingSequence(self) -> bool:
        return self._executingSequence

    @property
    def currentSequenceFrame(self) -> fseqf.FightSequenceFrame:
        return self._currentSequenceFrame

    @property
    def slaveId(self) -> float:
        return self._slaveId

    @property
    def masterId(self) -> float:
        return self._masterId

    def pushed(self) -> bool:
        self._turnFrame = FightTurnFrame()
        self._sequenceFrames = []
        DataMapProvider().isInFight = True
        Kernel().worker.addFrame(self._turnFrame)
        self._destroyed = False
        self._neverSynchronizedBefore = True
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightTurnListMessage):
            gftmsg = msg
            if self._executingSequence or self._currentSequenceFrame:
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
                        and not Kernel().fightEntitiesFrame.getEntityInfos(fighter.contextualId)
                    ):
                        Kernel().fightEntitiesFrame.addOrUpdateActor(fighter)
            if self._executingSequence:
                self._synchroniseFighters = gftcimsg.fighters
                self._synchroniseFightersInstanceId = fseqf.FightSequenceFrame.currentInstanceId
            else:
                self.gameFightSynchronize(gftcimsg.fighters)
            return True

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

        elif isinstance(msg, SlaveNoLongerControledMessage):
            snlcmsg = msg
            playerId = PlayedCharacterManager().id
            if snlcmsg.masterId != playerId and self._slaveId == snlcmsg.slaveId:
                self._masterId = playerId
                self._slaveId = self._masterId
                self._slaveId = 0
            return False

        elif isinstance(msg, SequenceStartMessage):
            self._autoEndTurn = False
            if not self._sequenceFrameSwitcher:
                self._sequenceFrameSwitcher = FightSequenceSwitcherFrame()
                Kernel().worker.addFrame(self._sequenceFrameSwitcher)
            self._currentSequenceFrame = fseqf.FightSequenceFrame(self, self._currentSequenceFrame)
            self._sequenceFrameSwitcher.currentFrame = self._currentSequenceFrame
            return False

        elif isinstance(msg, SequenceEndMessage):
            semsg = msg
            if not self._currentSequenceFrame:
                Logger().warn("Got a Sequence End but no Sequence Start!")
                return True
            self._currentSequenceFrame.mustAck = semsg.authorId == int(CurrentPlayedFighterManager().currentFighterId)
            self._currentSequenceFrame.ackIdent = semsg.actionId
            self._sequenceFrameSwitcher.currentFrame = None
            if not self._currentSequenceFrame.parent:
                Kernel().worker.removeFrame(self._sequenceFrameSwitcher)
                self._sequenceFrameSwitcher = None
                self._sequenceFrames.append(self._currentSequenceFrame)
                self._currentSequenceFrame = None
                self.executeNextSequence()
            else:
                self._currentSequenceFrame.execute()
                self._sequenceFrameSwitcher.currentFrame = self._currentSequenceFrame.parent
                self._currentSequenceFrame = self._currentSequenceFrame.parent
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
            if GameDebugManager().buffsDebugActivated:
                Logger().info(f"[BUFFS DEBUG] Start of turn {self._turnsCount} !")
            bffm.BuffManager().spellBuffsToIgnore = []
            return True

        elif isinstance(msg, GameFightLeaveMessage):
            gflmsg = msg
            fighterInfos2 = Kernel().fightEntitiesFrame.getEntityInfos(self._lastPlayerId)
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
            while self._currentSequenceFrame and maxEndRescue > 0:
                Logger().error("/!\\ Fight end but no SequenceEnd was received")
                seqEnd = SequenceEndMessage()
                seqEnd.init(0, 0, 0)
                self.process(seqEnd)
            if self._executingSequence:
                Logger().error("Delaying fight end because we're still in a sequence.")
                self._endBattle = True
                self._battleResults = gfemsg
            else:
                self.endBattle(gfemsg)
            FightersStateManager().endFight()
            CurrentPlayedFighterManager().endFight()
            return False

        elif isinstance(msg, GameContextDestroyMessage):
            if self._battleResults:
                Logger().debug("Proper end of combat propre (resultats known)")
                self.endBattle(self._battleResults)
            else:
                Logger().debug("Brutal end of combat (no resultats known)")
                self._executingSequence = False
                fakegfemsg = GameFightEndMessage()
                fakegfemsg.init(0, 0, 0, None, [])
                self.process(fakegfemsg)
            return False

        elif isinstance(msg, GameFightPauseMessage):
            if msg.isPaused:
                Logger().debug("The fight is paused.")
            else:
                Logger().debug("The fight is resuming after pause.")
            self._fightIsPaused = msg.isPaused
            return True

        elif isinstance(msg, ApplySpellModifierMessage):
            SpellModifiersManager().setRawSpellModifier(msg.actorId, msg.modifier)
            return True

        elif isinstance(msg, RemoveSpellModifierMessage):
            SpellModifiersManager().deleteSpellModifierAction(msg.actorId, msg.modifierType, msg.actionType)
            return True

        elif isinstance(msg, GameFightTurnEndMessage):
            if not self._confirmTurnEnd:
                self._lastPlayerId = msg.id
            else:
                self._nextLastPlayerId = msg.id
            entityInfos = Kernel().fightEntitiesFrame.getEntityInfos(msg.id)
            if isinstance(entityInfos, GameFightFighterInformations) and not entityInfos.spawnInfo.alive:
                bffm.BuffManager().markFinishingBuffs(msg.id)
                if msg.id == CurrentPlayedFighterManager().currentFighterId:
                    CurrentPlayedFighterManager().getSpellCastManager().nextTurn()
                    SpellWrapper.refreshAllPlayerSpellHolder(msg.id)
            if msg.id == CurrentPlayedFighterManager().currentFighterId:
                self._turnFrame.myTurn = False
            return True

        else:
            return False

    def pulled(self) -> bool:
        self.applyDelayedStats()
        DataMapProvider().isInFight = False
        if Kernel().worker.contains("FightTurnFrame"):
            Kernel().worker.removeFrameByName("FightTurnFrame")
        if Kernel().worker.contains("FightSequenceFrame"):
            Kernel().worker.removeFrameByName("FightSequenceFrame")
        bffm.BuffManager.clear()
        self._currentSequenceFrame = None
        self._sequenceFrameSwitcher = None
        self._turnFrame = None
        self._battleResults = None
        self._newTurnsList = None
        self._newDeadTurnsList = None
        self._turnsList = None
        self.deadTurnsList = None
        self._sequenceFrames = None
        self._masterId = 0
        self._slaveId = 0
        self._skipTurnTimer = None
        self._destroyed = True
        KernelEventsManager().send(KernelEvent.FightEnded)
        return True

    def getSequencesStack(self) -> list[fseqf.FightSequenceFrame]:
        res = []
        seq = self._currentSequenceFrame
        while seq:
            res.insert(0, seq)
            seq = seq._parent
        return res

    def logState(self):
        Logger().separator("Current Sequences state")
        Logger().debug(f"Executing a sequence : {self._executingSequence}")
        Logger().debug(
            f"Sequence cached : #{self._sequenceFrameCached._instanceId if self._sequenceFrameCached else 'None'}"
        )
        Logger().debug(
            f"Sequence current : #{self._currentSequenceFrame._instanceId if self._currentSequenceFrame else 'None'}"
        )
        padd = ""
        res = self.getSequencesStack()
        for seq in res:
            Logger().debug(f"{padd}|---> Sequence #{seq._instanceId}")
            for step in seq._stepsBuffer:
                Logger().debug(f"{padd}\t|---> {step.__class__.__name__}")
            padd += "\t"

    def delayCharacterStatsList(self, msg: CharacterStatsListMessage) -> None:
        self._delayCslmsg = msg

    def executeNextSequence(self) -> bool:
        if self._executingSequence:
            return False
        if self._sequenceFrames:
            nextSequenceFrame = self._sequenceFrames.pop(0)
            self._executingSequence = True
            nextSequenceFrame.execute(self.finishSequence(nextSequenceFrame))
            return True
        return False

    def applyDelayedStats(self) -> None:
        if not self._delayCslmsg:
            return
        pcuF.PlayedCharacterUpdatesFrame.updateCharacterStatsList(self._delayCslmsg.stats, True)
        self._delayCslmsg = None

    def sendAcknowledgement(self) -> None:
        if self._sequenceFrameCached is None:
            return
        ack: GameActionAcknowledgementMessage = GameActionAcknowledgementMessage()
        ack.init(True, self._sequenceFrameCached.ackIdent)
        CurrentPlayedFighterManager().conn.send(ack)
        self._sequenceFrameCached = None

    def finishSequence(self, sequenceFrame: fseqf.FightSequenceFrame) -> FunctionType:
        def function() -> None:
            if self._destroyed:
                return
            if sequenceFrame.mustAck:
                self._sequenceFrameCached = sequenceFrame
                self.sendAcknowledgement()
            self._executingSequence = False
            if self._sequenceFrames and self._sequenceFrames[0].instanceId >= self._synchroniseFightersInstanceId:
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
                Logger().warning("This fight must end ! Finishing things now.")
                self._endBattle = False
                self.endBattle(self._battleResults)
                self._battleResults = False
                return
            KernelEventsManager().send(KernelEvent.SequenceExecFinished)

        return function

    def sendAutoEndTurn(self, e) -> None:
        action: Action = None
        if self._autoEndTurn:
            action = GameFightTurnFinishAction()
            Kernel().worker.process(action)
            self._autoEndTurn = False

    def updateTurnsList(self, turnsList: list[float], deadTurnsList: list[float]) -> None:
        self._turnsList = turnsList
        self.deadTurnsList = deadTurnsList

    def endBattle(self, fightEnd: GameFightEndMessage) -> None:
        self._holder: FightEntitiesHolder = FightEntitiesHolder()
        self._holder.reset()
        self._synchroniseFighters = None
        Kernel().worker.removeFrame(self)
        fightContextFrame = Kernel().fightContextFrame
        fightContextFrame.process(fightEnd)

    def onSkipTurnTimeOut(self, event) -> None:
        self._skipTurnTimer.cancel()

    def gameFightSynchronize(self, fighters: list[GameFightFighterInformations]) -> None:
        newWaveAppeared: bool = False
        newWaveMonster: bool = False
        entitiesFrame = Kernel().fightEntitiesFrame
        newWaveMonsterIndex: int = 0
        bffm.BuffManager().synchronize()
        for fighterInfos in fighters:
            if fighterInfos.spawnInfo.alive:
                newWaveMonster = (
                    fighterInfos.wave == self._newWaveId
                    and fighterInfos.wave != 0
                    and not DofusEntities().getEntity(fighterInfos.contextualId)
                )
                entitiesFrame.updateFighter(fighterInfos)
                StatsManager().addRawStats(
                    fighterInfos.contextualId, fighterInfos.stats.characteristics.characteristics
                )
                bffm.BuffManager().markFinishingBuffs(fighterInfos.contextualId, False)
                for buff in bffm.BuffManager().getAllBuff(fighterInfos.contextualId):
                    if isinstance(buff, StatBuff):
                        buff.isRecent = False
                if newWaveMonster:
                    newWaveAppeared = True
                    DofusEntities().getEntity(fighterInfos.contextualId).visible = False
                    Kernel().worker.terminated.wait(0.3 * newWaveMonsterIndex)
                    entity = DofusEntities().getEntity(self._fighterId)
                    if entity:
                        entity.visible = self._visibility
                    newWaveMonsterIndex += 1
        if newWaveAppeared:
            self._newWave = False
            self._newWaveId = -1
        if self._neverSynchronizedBefore:
            self._neverSynchronizedBefore = False

    def removeSavedPosition(self, pEntityId: float) -> None:
        fightContextFrame = Kernel().fightContextFrame
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
