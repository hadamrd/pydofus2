from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class PrismInformation(NetworkMessage):
    state: int
    placementDate: int
    nuggetsCount: int
    durability: int
    nextEvolutionDate: int

    def init(self, state_: int, placementDate_: int, nuggetsCount_: int, durability_: int, nextEvolutionDate_: int):
        self.state = state_
        self.placementDate = placementDate_
        self.nuggetsCount = nuggetsCount_
        self.durability = durability_
        self.nextEvolutionDate = nextEvolutionDate_

        super().__init__()
