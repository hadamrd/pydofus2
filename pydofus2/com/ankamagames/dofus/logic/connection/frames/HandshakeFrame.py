from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.network.messages.common.basic.BasicPingMessage import BasicPingMessage
from pydofus2.com.ankamagames.dofus.network.messages.handshake.ProtocolRequired import ProtocolRequired
from pydofus2.com.ankamagames.dofus.network.Metadata import Metadata
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectedMessage import ConnectedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class HandshakeFrame(Frame):

    TIMEOUT_DELAY: int = 30
    TIMEOUT_REPEAT_COUNT: int = 1

    def __init__(self):
        self._timeoutTimer = None
        super().__init__()

    def checkProtocolVersions(self, serverVersion: str) -> None:
        Logger().info(f"[HandShake] Server version is {serverVersion}. Client version is {Metadata.PROTOCOL_BUILD}.")
        if serverVersion != Metadata.PROTOCOL_BUILD:
            KernelEventsManager().send(
                KernelEvent.ClientCrashed, "Protocol mismatch between the client and the server."
            )
            return

    def extractHashFromProtocolVersion(self, protocolVersion: str) -> str:
        if not protocolVersion:
            return None
        matches: list = protocolVersion.split("-")
        if matches is None or len(matches) < 2:
            return None
        return matches[1]

    @property
    def priority(self) -> int:
        return Priority.HIGHEST

    def pushed(self) -> bool:
        ConnectionsHandler().hasReceivedNetworkMsg = False
        return True

    def process(self, msg: Message) -> bool:
        ConnectionsHandler().hasReceivedMsg = True

        if isinstance(msg, INetworkMessage):
            ConnectionsHandler().hasReceivedNetworkMsg = True
            if self._timeoutTimer:
                self._timeoutTimer.cancel()

        if isinstance(msg, ProtocolRequired):
            prmsg = msg
            self.checkProtocolVersions(prmsg.version)
            Kernel().worker.removeFrame(self)
            return True

        elif isinstance(msg, ConnectedMessage):
            self._timeoutTimer = BenchmarkTimer(self.TIMEOUT_DELAY, self.onTimeout)
            self._timeoutTimer.start()
            return True

        return False

    def onTimeout(self) -> None:
        pingMsg = BasicPingMessage()
        pingMsg.init(True)
        ConnectionsHandler().send(pingMsg)

    def pulled(self) -> bool:
        if self._timeoutTimer:
            self._timeoutTimer.cancel()
        return True
