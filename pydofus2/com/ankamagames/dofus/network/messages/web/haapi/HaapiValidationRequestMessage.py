from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class HaapiValidationRequestMessage(NetworkMessage):
    transaction: str

    def init(self, transaction_: str):
        self.transaction = transaction_

        super().__init__()
