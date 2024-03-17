from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ExchangeStartOkRecycleTradeMessage(NetworkMessage):
    percentToPrism: int
    percentToPlayer: int
    adjacentSubareaPossessed: list[int]
    adjacentSubareaUnpossessed: list[int]
    def init(self, percentToPrism_: int, percentToPlayer_: int, adjacentSubareaPossessed_: list[int], adjacentSubareaUnpossessed_: list[int]):
        self.percentToPrism = percentToPrism_
        self.percentToPlayer = percentToPlayer_
        self.adjacentSubareaPossessed = adjacentSubareaPossessed_
        self.adjacentSubareaUnpossessed = adjacentSubareaUnpossessed_
        
        super().__init__()
    