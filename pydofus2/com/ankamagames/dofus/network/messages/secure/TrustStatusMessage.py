from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class TrustStatusMessage(NetworkMessage):
    certified: bool

    def init(self, certified_: bool):
        self.certified = certified_

        super().__init__()
