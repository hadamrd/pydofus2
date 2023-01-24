import threading
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager, KernelEvts
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReason import DisconnectionReason
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from time import perf_counter, sleep
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import (
    DisconnectionReasonEnum,
)
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import (
    LoginValidationWithTokenAction,
)
import pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager as auth
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.jerakine.data.I18nFileAccessor import I18nFileAccessor
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.network.ServerConnection import ServerConnection
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider

logger = Logger()

class DofusClient(threading.Thread):
    
    def __init__(self, name="unknown"):
        super().__init__(name=name)
        self._killSig = threading.Event()
    
    def init(self):
        self._stopReason: DisconnectionReason = None
        self._lastLoginTime = None
        self._minLoginInterval = 10
        self._worker = Kernel().worker
        self._registredInitFrames = []
        self._registredGameStartFrames = []
        Kernel().init()
        I18nFileAccessor()
        DataMapProvider()
        KernelEventsManager().once(KernelEvts.CHARACTER_SELECTION_SUCCESS, self._onCharacterSelectionSuccess)
        KernelEventsManager().once(KernelEvts.CRASH, self._onCrash)
        KernelEventsManager().once(KernelEvts.SHUTDOWN, self._onShutdown)
        KernelEventsManager().once(KernelEvts.RESTART, self._onRestart)
        logger.info("[DofusClient] initialized")

    def login(self, loginToken, serverId=0, characterId=None):
        self._serverId = serverId
        self._characterId = characterId
        self._loginToken = loginToken
        self.start()

    def registerInitFrame(self, frame):
        self._registredInitFrames.append(frame)

    def registerGameStartFrame(self, frame):
        self._registredGameStartFrames.append(frame)

    def _onCharacterSelectionSuccess(self, event):
        for frame in self._registredGameStartFrames:
            self._worker.addFrame(frame())
    
    def _onCrash(self, event, message):
        self._killSig.set()
        logger.debug(f"[DofusClient] Crashed for reason: {message}")
    
    def _onShutdown(self, event, message):
        self._killSig.set()
        logger.debug(f"[DofusClient] Shutdown requested for reason: {message}")
    
    def _onRestart(self, event, message):
        logger.debug(f"[DofusClient] Restart requested for reason: {message}")
        
    def shutdown(self, reason=DisconnectionReasonEnum.WANTED_SHUTDOWN, msg=""):
        logger.info("Shuting down ...")
        ConnectionsHandler().closeConnection(reason, msg)

    def relogin(self):
        self.login(self._loginToken, self._serverId, self._characterId)

    @property
    def connection(self) -> "ServerConnection":
        return ConnectionsHandler().conn
    
    @property
    def registeredInitFrames(self) -> list:
        return self._registredInitFrames

    @property
    def registeredGameStartFrames(self) -> list:
        return self._registredGameStartFrames

    def run(self):
        logger.debug(f"current thread: {threading.current_thread().name}")
        self.init()
        try:
            if self._lastLoginTime is not None and perf_counter() - self._lastLoginTime < self._minLoginInterval:
                logger.info("[DofusClient] Login request too soon, will wait some time")
                sleep(self._minLoginInterval - (perf_counter() - self._lastLoginTime))
            self._lastLoginTime = perf_counter()
            if Kernel().reseted:
                Kernel().init()
            auth.AuthentificationManager().setToken(self._loginToken)
            if self._characterId:
                PlayerManager().allowAutoConnectCharacter = True
                PlayedCharacterManager().id = self._characterId
                PlayerManager().autoConnectOfASpecificCharacterId = self._characterId
            for frame in self._registredInitFrames:
                self._worker.addFrame(frame())
            if self._serverId == 0:
                self._worker.processImmediately(
                    LoginValidationWithTokenAction.create(autoSelectServer=False, serverId=self._serverId)
                )
            else:
                self._worker.processImmediately(
                    LoginValidationWithTokenAction.create(autoSelectServer=True, serverId=self._serverId)
                )
            while not self._killSig.is_set():
                msg = ConnectionsHandler().conn.receive()
                self._worker.process(msg)
        except:
            logger.error(f"[DofusClient] Error in main loop.", exc_info=True)
        logger.info("[DofusClient] Stopped")
