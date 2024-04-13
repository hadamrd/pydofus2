from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import LeaveDialogMessage


class ExchangeLeaveMessage(LeaveDialogMessage):
    success: bool

    def init(self, success_: bool, dialogType_: int):
        self.success = success_

        super().init(dialogType_)
