from time import perf_counter

import pydofus2.com.ankamagames.dofus.logic.game.approach.frames.GameServerApproachFrame as gsaF
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import \
    DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.frames.QueueFrame import \
    QueueFrame
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import \
    LoginValidationWithTokenAction as LVA_WithToken
from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthentificationFrame import \
    AuthentificationFrame
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import \
    AuthentificationManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectionProcessCrashedMessage import \
    ConnectionProcessCrashedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.messages.WrongSocketClosureReasonMessage import \
    WrongSocketClosureReasonMessage
from pydofus2.com.ankamagames.jerakine.network.messages.UnexpectedSocketClosureMessage import \
    UnexpectedSocketClosureMessage
from pydofus2.com.ankamagames.jerakine.network.ServerConnectionClosedMessage import \
    ServerConnectionClosedMessage
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class DisconnectionHandlerFrame(Frame):
    MAX_CONN_TRIES = 3

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.LOW

    def pushed(self) -> bool:
        self._connectionUnexpectedFailureTimes = []
        self._conxTries = 0
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, ServerConnectionClosedMessage):
            reason = ConnectionsHandler().handleDisconnection()
            Logger().info(f"Connection '{msg.closedConnection}' closed for reason : {reason}")
            if ConnectionsHandler().hasReceivedMsg:
                if (
                    not reason.expected
                    and not ConnectionsHandler().hasReceivedNetworkMsg
                    and self._conxTries < self.MAX_CONN_TRIES
                ):
                    Logger().error(
                        f"The connection was closed unexpectedly. Reconnection attempt {self._conxTries}/{self.MAX_CONN_TRIES}."
                    )
                    self._conxTries += 1
                    self._connectionUnexpectedFailureTimes.append(perf_counter())
                    KernelEventsManager().send(KernelEvent.ClientRestart, reason.message)
                else:
                    if not reason.expected:
                        self._connectionUnexpectedFailureTimes.append(perf_counter())
                        KernelEventsManager().send(
                            KernelEvent.ClientRestart, "The connection was closed unexpectedly."
                        )
                    else:
                        if reason.type in [DisconnectionReasonEnum.EXCEPTION_THROWN, DisconnectionReasonEnum.BANNED]:
                            KernelEventsManager().send(KernelEvent.ClientCrashed, reason.message, reason.type)
                        elif reason.type == DisconnectionReasonEnum.WANTED_SHUTDOWN:
                            KernelEventsManager().send(KernelEvent.ClientShutdown, reason.type, reason.message)
                        elif reason.type in [
                            DisconnectionReasonEnum.RESTARTING,
                            DisconnectionReasonEnum.DISCONNECTED_BY_POPUP,
                            DisconnectionReasonEnum.CONNECTION_LOST,
                        ]:
                            KernelEventsManager().send(KernelEvent.ClientRestart, reason.message)
                        elif reason.type == DisconnectionReasonEnum.SWITCHING_TO_GAME_SERVER:
                            Kernel().worker.addFrame(gsaF.GameServerApproachFrame())
                            ConnectionsHandler().connectToGameServer(
                                Kernel().serverSelectionFrame.selectedServer.address,
                                Kernel().serverSelectionFrame.selectedServer.ports[0],
                            )
                        elif reason.type == DisconnectionReasonEnum.CHANGING_SERVER:
                            lva = AuthentificationManager()._lva
                            targetServerId = lva.serverId if lva else None
                            if targetServerId is None:
                                Logger().error(
                                    f"Closed connection to change server but no serverId is specified in Auth Manager"
                                )
                            else:
                                Logger().info(f"Switching to target server {targetServerId} server ...")
                                Kernel().worker.addFrame(AuthentificationFrame())
                                Kernel().worker.addFrame(QueueFrame())
                                lva = LVA_WithToken.create(targetServerId != 0, targetServerId)
                                Kernel().worker.process(lva)

                        elif reason.type == DisconnectionReasonEnum.SWITCHING_TO_HUMAN_VENDOR:
                            pass

                        elif reason.type == DisconnectionReasonEnum.DISCONNECTED_BY_USER:
                            pass
            else:
                Logger().warning("The connection hasn't even start or already closed.")
            KernelEventsManager().send(KernelEvent.ClientClosed, msg.closedConnection)
            return True

        elif isinstance(msg, WrongSocketClosureReasonMessage):
            wscrmsg = msg
            Logger().error(
                "Expecting socket closure for reason "
                + str(wscrmsg.expectedReason)
                + ", got reason "
                + str(wscrmsg.gotReason)
                + "! Reseting."
            )
            Kernel().reset([UnexpectedSocketClosureMessage()])
            return True

        elif isinstance(msg, UnexpectedSocketClosureMessage):
            Logger().debug("Got hook UnexpectedSocketClosure")
            KernelEventsManager().send(
                KernelEvent.ClientCrashed,
                message="Unexpected socket closure",
                reason=DisconnectionReasonEnum.UNEXPECTED,
            )
            return True

        elif isinstance(msg, ConnectionProcessCrashedMessage):
            KernelEventsManager().send(
                KernelEvent.ClientCrashed, message=msg.err, reason=DisconnectionReasonEnum.CONNECTION_PROCESS_CRASHED
            )
            return True

    def pulled(self) -> bool:
        return True
