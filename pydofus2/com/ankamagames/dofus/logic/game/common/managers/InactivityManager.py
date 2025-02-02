from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.communication.InfoMessage import InfoMessage
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.FeatureManager import FeatureManager
from pydofus2.com.ankamagames.dofus.network.messages.common.basic.BasicPingMessage import BasicPingMessage
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.metaclass.Singleton import Singleton  # Assuming a logger module exists


class InactivityManager(metaclass=Singleton):
    SERVER_INACTIVITY_DELAY = 10 * 60
    SERVER_INACTIVITY_SPEED_PING_DELAY = 5
    INACTIVITY_DELAY = 5 * 60
    INACTIVITY_DELAY_WARNING_POPUP = 20 * 60
    MESSAGE_TYPE_ID = 4
    DISCONNECTED_FOR_INACTIVITY_MESSAGE_ID = 1

    def __init__(self):
        self.popupApi = None  # Replace with actual PopupApi
        self._isAfk = False
        self._inactivityTimer = BenchmarkTimer(self.INACTIVITY_DELAY, self.onActivityTimerUp)
        self._inactivityWarningPopupTimer = BenchmarkTimer(
            self.INACTIVITY_DELAY_WARNING_POPUP, self.onActivityPopupTimerUp
        )
        self._serverActivityTimer = BenchmarkTimer(self.SERVER_INACTIVITY_DELAY, self.onServerActivityTimerUp)
        self._paused = False
        self._hasActivity = False
        self.resetActivity()
        self.resetServerActivity()

    @staticmethod
    def server_notification():
        if ConnectionsHandler().conn.connected.is_set():
            msg = BasicPingMessage()
            msg.init(True)
            ConnectionsHandler().send(msg)

    @property
    def inactivity_delay(self):
        return self._inactivityTimer.interval

    @inactivity_delay.setter
    def inactivity_delay(self, t):
        self._inactivityTimer.interval = t
        self.resetActivity()

    def start(self):
        self.resetActivity()
        self.resetServerActivity()
        self._isAfk = False

    def stop(self, clear_callback=None):
        self._inactivityWarningPopupTimer.cancel()
        self._inactivityTimer.cancel()
        self._serverActivityTimer.cancel()

    def update_server_inactivity_delay(self):
        server_inactivity_delay = self.SERVER_INACTIVITY_DELAY
        if FeatureManager().isFeatureWithKeywordEnabled("FAST_PING"):
            server_inactivity_delay = self.SERVER_INACTIVITY_SPEED_PING_DELAY
        self._serverActivityTimer.cancel()
        self._serverActivityTimer = BenchmarkTimer(server_inactivity_delay, self.onServerActivityTimerUp)
        self.resetServerActivity()

    def pause(self, paused):
        self._paused = paused
        self.resetActivity()

    def resetActivity(self):
        self._inactivityWarningPopupTimer.cancel()
        self._inactivityTimer.cancel()
        if not self._paused:
            self._inactivityWarningPopupTimer = BenchmarkTimer(
                self.INACTIVITY_DELAY_WARNING_POPUP, self.onActivityPopupTimerUp
            )
            self._inactivityWarningPopupTimer.start()
            self._inactivityTimer = BenchmarkTimer(self.INACTIVITY_DELAY, self.onActivityTimerUp)
            self._inactivityTimer.start()

    def resetServerActivity(self):
        self._serverActivityTimer.cancel()
        self._serverActivityTimer = BenchmarkTimer(self.SERVER_INACTIVITY_DELAY, self.onServerActivityTimerUp)
        self._serverActivityTimer.start()

    def activity(self):
        self.resetActivity()
        self._hasActivity = True
        if self._isAfk:
            self._isAfk = False
            KernelEventsManager().send(KernelEvent.InactivityNotification, False)

    def onActivityPopupTimerUp(self):
        self._isAfk = True
        KernelEventsManager().send(KernelEvent.InactivityNotification, True)

    def onActivityTimerUp(self):
        inactivity_message_text = InfoMessage.getInfoMessageById(
            self.MESSAGE_TYPE_ID * 10000 + self.DISCONNECTED_FOR_INACTIVITY_MESSAGE_ID
        ).text
        KernelEventsManager().send(KernelEvent.ClientRestart, inactivity_message_text)

    def onServerActivityTimerUp(self):
        if self._hasActivity:
            self._hasActivity = False
            self.server_notification()
        self.resetServerActivity()


# Example usage:
# inactivity_manager = InactivityManager.get_instance()
# inactivity_manager.start()
