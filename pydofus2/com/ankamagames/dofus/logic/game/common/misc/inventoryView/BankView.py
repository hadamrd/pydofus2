from pydofus2.com.ankamagames.dofus.logic.game.common.managers.StorageOptionManager import StorageOptionManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.inventoryView.StorageGenericView import StorageGenericView


class BankView(StorageGenericView):

    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "bank"

    def updateView(self) -> None:
        super().updateView()

    def sortFields(self) -> list:
        return StorageOptionManager().sortBankFields

    def sortRevert(self) -> bool:
        return StorageOptionManager().sortBankRevert
