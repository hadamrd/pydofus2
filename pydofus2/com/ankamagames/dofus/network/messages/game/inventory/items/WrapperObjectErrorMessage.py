from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.items.SymbioticObjectErrorMessage import (
    SymbioticObjectErrorMessage,
)


class WrapperObjectErrorMessage(SymbioticObjectErrorMessage):
    def init(self, errorCode_: int, reason_: int):

        super().init(errorCode_, reason_)
