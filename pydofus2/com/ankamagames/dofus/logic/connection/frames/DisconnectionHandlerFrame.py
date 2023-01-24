from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager, KernelEvts
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from time import perf_counter
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
import pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler as connh
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import (
    DisconnectionReasonEnum as Reason,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectionProcessCrashedMessage import ConnectionProcessCrashedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.messages.WrongSocketClosureReasonMessage import (
    WrongSocketClosureReasonMessage,
)
from pydofus2.com.ankamagames.jerakine.network.ServerConnectionClosedMessage import (
    ServerConnectionClosedMessage,
)
from pydofus2.com.ankamagames.jerakine.network.messages.ExpectedSocketClosureMessage import (
    ExpectedSocketClosureMessage,
)
from pydofus2.com.ankamagames.jerakine.network.messages.UnexpectedSocketClosureMessage import (
    UnexpectedSocketClosureMessage,
)
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
import pydofus2.com.ankamagames.dofus.logic.game.approach.frames.GameServerApproachFrame as gsaF

logger = Logger("Dofus2")


class DisconnectionHandlerFrame(Frame):

    MAX_TRIES: int = 4

    def __init__(self):
        self._connectionUnexpectedFailureTimes = list()
        self._timer: BenchmarkTimer = None
        self._conxTries: int = 0
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.LOW

    def resetConnectionAttempts(self) -> None:
        self._connectionUnexpectedFailureTimes = list()
        self._conxTries = 0

    def pushed(self) -> bool:
        logger.debug("DisconnectionHandlerFrame pushed")
        return True

    def handleUnexpectedNoMsgReceived(self):
        self._conxTries += 1
        logger.warn(
            f"The connection was closed unexpectedly. Reconnection attempt {self._conxTries}/{self.MAX_TRIES} will start in 4s."
        )
        self._connectionUnexpectedFailureTimes.append(perf_counter())
        self._timer = BenchmarkTimer(4, self.reconnect)
        self._timer.start()

    @property
    def connection(self):
        return self.connHandle.conn
    
    @property
    def connHandle(self):
        return connh.ConnectionsHandler()
    
    def process(self, msg: Message) -> bool:

        if isinstance(msg, ServerConnectionClosedMessage):
            gsaF.GameServerApproachFrame.authenticationTicketAccepted = False
            reason = self.connHandle.handleDisconnection()
            if self.connHandle.hasReceivedMsg:
                if not reason.expected and not self.connHandle.hasReceivedNetworkMsg and self._conxTries < self.MAX_TRIES:
                    self.handleUnexpectedNoMsgReceived()
                else:
                    if not reason.expected:
                        logger.debug(f"The connection was closed unexpectedly. Reseting.")
                        self._connectionUnexpectedFailureTimes.append(perf_counter())
                        if self._timer:
                            self._timer.cancel()
                        self._timer = BenchmarkTimer(10, self.reconnect)
                        self._timer.start()
                    else:
                        if (reason.reason == Reason.SWITCHING_TO_HUMAN_VENDOR
                            or reason.reason == Reason.WANTED_SHUTDOWN
                            or reason.reason == Reason.EXCEPTION_THROWN
                        ):
                            if reason.reason == Reason.EXCEPTION_THROWN:
                                KernelEventsManager().send(KernelEvts.CRASH, message=reason.message)
                            else:
                                KernelEventsManager().send(KernelEvts.SHUTDOWN, message=reason.message)
                        elif reason.reason == Reason.RESTARTING or \
                            reason.reason == Reason.DISCONNECTED_BY_POPUP or \
                            reason.reason == Reason.CONNECTION_LOST:
                            KernelEventsManager().send(KernelEvts.RESTART, message=reason.message)
                        else:
                            Kernel().worker.process(ExpectedSocketClosureMessage(reason.reason))
            else:
                logger.warn("The connection hasn't even start.")
            return True

        elif isinstance(msg, WrongSocketClosureReasonMessage):
            wscrmsg = msg
            gsaF.GameServerApproachFrame.authenticationTicketAccepted = False
            logger.error(
                "Expecting socket closure for reason "
                + str(wscrmsg.expectedReason)
                + ", got reason "
                + str(wscrmsg.gotReason)
                + "! Reseting."
            )
            Kernel().reset([UnexpectedSocketClosureMessage()])
            return True

        elif isinstance(msg, UnexpectedSocketClosureMessage):
            logger.debug("got hook UnexpectedSocketClosure")
            gsaF.GameServerApproachFrame.authenticationTicketAccepted = False
            KernelEventsManager().send(KernelEvts.CRASH, message="Unexpected socket closure")
            return True

        elif isinstance(msg, ConnectionProcessCrashedMessage):
            logger.debug("Connection process crashed with error : " + msg.err)
            gsaF.GameServerApproachFrame.authenticationTicketAccepted = False
            raise Exception(msg.err)

    def reconnect(self) -> None:
        logger.debug("Reconnecting...")
        Kernel().reset(reloadData=True, autoRetry=True)

    def pulled(self) -> bool:
        return True
