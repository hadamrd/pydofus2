from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class BasicPongMessage(NetworkMessage):
    quiet: bool

    def init(self, quiet_: bool):
        self.quiet = quiet_

        super().__init__()
