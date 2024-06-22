from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.SymbioticObjectAssociatedMessage import (
    SymbioticObjectAssociatedMessage,
)


class MimicryObjectAssociatedMessage(SymbioticObjectAssociatedMessage):
    def init(self, hostUID_: int):

        super().init(hostUID_)
