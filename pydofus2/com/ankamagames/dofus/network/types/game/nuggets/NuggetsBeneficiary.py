from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class NuggetsBeneficiary(NetworkMessage):
    beneficiaryPlayerId: int
    nuggetsQuantity: int

    def init(self, beneficiaryPlayerId_: int, nuggetsQuantity_: int):
        self.beneficiaryPlayerId = beneficiaryPlayerId_
        self.nuggetsQuantity = nuggetsQuantity_

        super().__init__()
