from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class NuggetsInformationMessage(NetworkMessage):
    nuggetsQuantity: int

    def init(self, nuggetsQuantity_: int):
        self.nuggetsQuantity = nuggetsQuantity_

        super().__init__()
