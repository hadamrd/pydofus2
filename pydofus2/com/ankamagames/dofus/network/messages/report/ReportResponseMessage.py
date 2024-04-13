from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ReportResponseMessage(NetworkMessage):
    success: bool

    def init(self, success_: bool):
        self.success = success_

        super().__init__()
