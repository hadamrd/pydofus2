from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
import pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler as connh
from pydofus2.com.ankamagames.dofus.network.Metadata import Metadata
from pydofus2.com.ankamagames.dofus.network.messages.common.basic.BasicPingMessage import (
    BasicPingMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.handshake.ProtocolRequired import (
    ProtocolRequired,
)
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectedMessage import ConnectedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.dofus.kernel.PanicMessages import PanicMessages

logger = Logger("Dofus2")


class HandshakeFrame(Frame):

    TIMEOUT_DELAY: int = 3000

    TIMEOUT_REPEAT_COUNT: int = 1

    def __init__(self):
        self._timeoutTimer = None
        super().__init__()

    def checkProtocolVersions(self, serverVersion: str) -> None:
        logger.info("Server version is " + serverVersion + ". Client version is " + Metadata.PROTOCOL_BUILD + ".")
        if not serverVersion or not Metadata.PROTOCOL_BUILD:
            logger.fatal("A protocol version is empty or None. What happened?")
            krnl.Kernel().panic(
                PanicMessages.MALFORMED_PROTOCOL,
                [Metadata.PROTOCOL_BUILD, serverVersion],
            )
            return
        clientHash: str = self.extractHashFromProtocolVersion(Metadata.PROTOCOL_BUILD)
        if not clientHash:
            logger.fatal("The client protocol version is malformed: " + Metadata.PROTOCOL_BUILD)
            krnl.Kernel().panic(
                PanicMessages.MALFORMED_PROTOCOL,
                [Metadata.PROTOCOL_BUILD, serverVersion],
            )
            return
        serverHash: str = self.extractHashFromProtocolVersion(serverVersion)
        if not serverHash:
            logger.fatal("The server protocol version is malformed: " + serverVersion)
            krnl.Kernel().panic(
                PanicMessages.MALFORMED_PROTOCOL,
                [Metadata.PROTOCOL_BUILD, serverVersion],
            )
            return
        if clientHash != serverHash:
            logger.fatal("Protocol mismatch between the client and the server.")
            krnl.Kernel().panic(
                PanicMessages.PROTOCOL_MISMATCH,
                [Metadata.PROTOCOL_BUILD, serverVersion],
            )

    def extractHashFromProtocolVersion(self, protocolVersion: str) -> str:
        if not protocolVersion:
            return None
        matches: list = protocolVersion.split("-")
        if matches == None or len(matches) < 2:
            return None
        return matches[1]

    @property
    def priority(self) -> int:
        return Priority.HIGHEST

    def pushed(self) -> bool:
        connh.ConnectionsHandler().hasReceivedNetworkMsg = False
        return True

    def process(self, msg: Message) -> bool:
        connh.ConnectionsHandler().hasReceivedMsg = True

        if isinstance(msg, INetworkMessage):
            connh.ConnectionsHandler().hasReceivedNetworkMsg = True
            if self._timeoutTimer is not None:
                self._timeoutTimer.cancel()

        if isinstance(msg, ProtocolRequired):
            prmsg = msg
            self.checkProtocolVersions(prmsg.version)
            krnl.Kernel().getWorker().removeFrame(self)
            return True

        elif isinstance(msg, ConnectedMessage):
            self._timeoutTimer = BenchmarkTimer(self.TIMEOUT_DELAY, self.onTimeout)
            self._timeoutTimer.start()
            return True

        else:
            return False

    def onTimeout(self) -> None:
        pingMsg: BasicPingMessage = BasicPingMessage(quiet_=True)
        connh.ConnectionsHandler().conn.send(pingMsg)

    def pulled(self) -> bool:
        if self._timeoutTimer is not None:
            self._timeoutTimer = None
        return True
