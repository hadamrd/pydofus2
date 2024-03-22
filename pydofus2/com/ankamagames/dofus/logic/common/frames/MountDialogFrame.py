from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.network.enums.DialogTypeEnum import \
    DialogTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import \
    ExchangeLeaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeMountStableErrorMessage import \
    ExchangeMountStableErrorMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame


class MountDialogFrame(Frame):

    def __init__(self):
        super().__init__()
        self._inStable = False

    @property
    def priority(self):
        return 0

    @property
    def inStable(self):
        return self._inStable

    def pushed(self):
        self._inStable = True
        self.sendStartOkMount()
        return True

    def process(self, msg):
        if isinstance(msg, ExchangeMountStableErrorMessage):
            return True
        
        elif isinstance(msg, ExchangeLeaveMessage):
            elm = msg
            if elm.dialogType == DialogTypeEnum.DIALOG_EXCHANGE:
                Kernel().worker.removeFrame(self)
            return True
        
        else:
            return False

    def pulled(self):
        self._inStable = False
        KernelEventsManager().send(KernelEvent.ExchangeLeave, True)
        return True

    def sendStartOkMount(self):
        KernelEventsManager().send(KernelEvent.ExchangeStartOkMount, Kernel().mountFrame.stableList, Kernel().mountFrame.paddockList)
