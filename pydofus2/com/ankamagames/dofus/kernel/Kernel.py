from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.logic.common.frames.LatencyFrame import LatencyFrame
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import (
    AuthentificationManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import (
    FightersStateManager,
)
import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
from pydofus2.com.ankamagames.dofus.network.Metadata import Metadata
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.network.messages.Worker import Worker
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
logger = Logger("Dofus2")


class Kernel(metaclass=Singleton):
    
    def __init__(self) -> None:
        self._worker: Worker = Worker()
        self.beingInReconection: bool = False
        self._reseted = True

    def getWorker(self) -> Worker:
        return self._worker

    def panic(self, errorId: int = 0, panicArgs: list = None) -> None:
        from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import (
            ConnectionsHandler,
        )
        self._worker.clear()
        ConnectionsHandler().closeConnection()

    @property
    def wasReseted(self) -> bool:
        return self._reseted
    
    def init(self) -> None:
        self._worker.clear()
        self.addInitialFrames()
        self._reseted = False
        logger.info(f"Using protocole #{Metadata.PROTOCOL_BUILD}, built on {Metadata.PROTOCOL_DATE}")

    def reset(
        self,
        messagesToDispatchAfter: list = None,
        autoRetry: bool = False,
        reloadData: bool = False,
    ) -> None:
        import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager as cpfm
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import SpellModifiersManager
        from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
        from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
        from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
        if self._reseted:
            return None
        logger.debug("[KERNEL] Resetting ...")
        KernelEventsManager().reset()
        if not autoRetry:
            AuthentificationManager.clear()
        FightersStateManager.clear()
        cpfm.CurrentPlayedFighterManager.clear()
        DofusEntities.reset()
        ItemWrapper.clearCache()
        pcm.PlayedCharacterManager.clear()
        BenchmarkTimer.clear()
        StatsManager.clear()
        PlayerManager.clear()
        DataMapProvider.clear()
        ConnectionsHandler.clear()
        SpellModifiersManager.clear()
        self._worker.clear()
        if reloadData:
            self.addInitialFrames()
        self.beingInReconection = False
        if messagesToDispatchAfter is not None and len(messagesToDispatchAfter) > 0:
            for msg in messagesToDispatchAfter:
                self._worker.process(msg)
        self._reseted = True
        Kernel.clear()
        logger.debug("[KERNEL] Reseted")

    def addInitialFrames(self) -> None:
        import pydofus2.com.ankamagames.dofus.logic.connection.frames.DisconnectionHandlerFrame as dhF
        from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthentificationFrame import (
            AuthentificationFrame,
        )
        from pydofus2.com.ankamagames.dofus.logic.common.frames.CleanupCrewFrame import (
            CleanupCrewFrame,
        )
        from pydofus2.com.ankamagames.dofus.logic.common.frames.QueueFrame import QueueFrame

        logger.debug("[KERNEL] Adding initial frames ...")
        if not self._worker.contains("LatencyFrame"):
            self._worker.addFrame(LatencyFrame())
        self._worker.addFrame(AuthentificationFrame())
        self._worker.addFrame(QueueFrame())
        self._worker.addFrame(dhF.DisconnectionHandlerFrame())
        if not self._worker.contains("CleanupCrewFrame"):
            self._worker.addFrame(CleanupCrewFrame())
        logger.info("[KERNEL] initialized ...")

        