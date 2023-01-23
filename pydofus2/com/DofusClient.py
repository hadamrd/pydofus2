import signal
import subprocess
import sys
import threading
import tracemalloc
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReason import DisconnectionReason
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from time import perf_counter, sleep
import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import (
    DisconnectionReasonEnum,
)
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import (
    LoginValidationWithTokenAction,
)
import pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager as auth
import pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler as connh
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.data.I18nFileAccessor import I18nFileAccessor
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.jerakine.logger.MemoryProfiler import MemoryProfiler
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.network.ServerConnection import ServerConnection
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider

logger = Logger()

class DofusClient(metaclass=Singleton):
    
    def __init__(self, id="unknown"):
        super().__init__()
        self._stopReason: DisconnectionReason = None
        self._lastLoginTime = None
        self._minLoginInterval = 10
        self.id = id
        self._worker = krnl.Kernel().getWorker()
        self._registredInitFrames = []
        self._registredGameStartFrames = []
        krnl.Kernel().init()
        I18nFileAccessor()
        DataMapProvider()
        logger.info("DofusClient initialized")

    def login(self, loginToken, serverId=0, characterId=None):
        if self._lastLoginTime is not None and perf_counter() - self._lastLoginTime < self._minLoginInterval:
            logger.info("Login request too soon, will wait some time")
            sleep(self._minLoginInterval - (perf_counter() - self._lastLoginTime))
        if krnl.Kernel().wasReseted:
            krnl.Kernel().init()
        self._lastLoginTime = perf_counter()
        self._serverId = serverId
        self._characterId = characterId
        self._loginToken = loginToken
        auth.AuthentificationManager().setToken(self._loginToken)
        if characterId:
            PlayerManager().allowAutoConnectCharacter = True
            PlayedCharacterManager().id = characterId
            PlayerManager().autoConnectOfASpecificCharacterId = characterId
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

    def registerInitFrame(self, frame):
        self._registredInitFrames.append(frame)

    def registerGameStartFrame(self, frame):
        self._registredGameStartFrames.append(frame)

    def shutdown(self, reason=None, msg=""):
        logger.info("Shuting down ...")
        if reason is None:
            reason = DisconnectionReasonEnum.WANTED_SHUTDOWN
        self.ContentHandler.connectionGonnaBeClosed(reason, msg)
        self.connection.close()
        self.connection.join()

    def restart(self):
        connh.ConnectionsHandler().connectionGonnaBeClosed(DisconnectionReasonEnum.RESTARTING)
        connh.ConnectionsHandler().conn.close()

    def relogin(self):
        self.login(self._loginToken, self._serverId, self._characterId)

    @classmethod
    def interrupt(cls, reason: DisconnectionReason = None):
        cls._stopReason = reason
        cls.clear()

    @property
    def exitError(self) -> DisconnectionReason:
        return self._stopReason

    @property
    def connection(self) -> "ServerConnection":
        return connh.ConnectionsHandler().conn

    @property
    def ContentHandler(self):
        return connh.ConnectionsHandler()
    
    @property
    def registeredInitFrames(self) -> list:
        return self._registredInitFrames

    @property
    def registeredGameStartFrames(self) -> list:
        return self._registredGameStartFrames

class DofusClientThread(threading.Thread):
    LOG_MEMORY_USAGE: bool = False
    LOG_PERF = False
    
    def __init__(self, id="unknown"):
        super().__init__()
        self._killSig = threading.Event()
        self.name = id
        self.conn_pid = None
    
    @property
    def connProcess(self):
        return connh.ConnectionsHandler().conn
    
    def setLogin(self, loginToken, serverId=0, characterId=None):
        if self.LOG_MEMORY_USAGE:
            tracemalloc.start(3)
        self.loginToken = loginToken
        self.serverId = serverId
        self.characterId = characterId
    
    def relogin(self):
        if not self._killSig.is_set():
            raise Exception("Not implemented")
        
    def run(self):
        try:
            DofusClient().login(self.loginToken, self.serverId, self.characterId)
            while not self._killSig.is_set():
                msg = DofusClient().connection.receive()
                if not self.conn_pid:
                    self.conn_pid = self.connProcess.pid
                    logger.debug(f"[DofusClient] Connection process pid: {self.conn_pid}")
                if msg is None:
                    break
                DofusClient()._worker.process(msg)
                if self.LOG_MEMORY_USAGE:
                    snapshot = tracemalloc.take_snapshot()
                    MemoryProfiler.logMemoryUsage(snapshot)
        except Exception as e:
            logger.error(f"[DofusClient] Error in main loop.", exc_info=True)
        except KeyboardInterrupt:
            logger.info("[DofusClient] Keyboard interrupt")
        self.teardown()
        logger.info("DofusClient stopped")
    
    def teardown(self):
        logger.info("[DofusClient] Tearing down ...")
        krnl.Kernel().reset()
        if self.LOG_MEMORY_USAGE:
            MemoryProfiler.saveCollectedData()
        if DofusClient()._stopReason and DofusClient()._stopReason == DisconnectionReasonEnum.EXCEPTION_THROWN:
            raise Exception(DofusClient()._stopReason.message)
        logger.info("[DofusClient] Torn down")
        
    def stop(self):
        logger.debug("[DofusClient] Stopping DofusClient..")
        self._killSig.set()
