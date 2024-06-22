from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.houses.HouseSellRequestMessage import (
    HouseSellRequestMessage,
)


class HouseSellFromInsideRequestMessage(HouseSellRequestMessage):
    def init(self, instanceId_: int, amount_: int, forSale_: bool):

        super().init(instanceId_, amount_, forSale_)
