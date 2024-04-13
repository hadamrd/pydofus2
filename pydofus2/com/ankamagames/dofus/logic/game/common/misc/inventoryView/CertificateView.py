from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IInventoryView import IInventoryView
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class CertificateView(IInventoryView):

    _content: list[ItemWrapper]

    def __init__(self):
        super().__init__()

    def initialize(self, items: list[ItemWrapper]) -> None:
        self._content = list[ItemWrapper]()
        for item in items:
            if self.isListening(item):
                self.addItem(item, 0, False)
        self.updateView()

    @property
    def name(self) -> str:
        return "certificate"

    @property
    def content(self) -> list[ItemWrapper]:
        return self._content

    def addItem(self, item: ItemWrapper, invisible: int, needUpdateView: bool = True) -> None:
        self._content.insert(0, item)
        if needUpdateView:
            self.updateView()

    def removeItem(self, item: ItemWrapper, invisible: int) -> None:
        if item not in self.content:
            Logger().warn("L'item qui doit �tre supprim� n'est pas pr�sent dans la liste")
            return
        self.content.remove(item)
        self.updateView()

    def modifyItem(self, item: ItemWrapper, oldItem: ItemWrapper, invisible: int) -> None:
        self.updateView()

    def isListening(self, item: ItemWrapper) -> bool:
        return item.isCertificate

    def updateView(self) -> None:
        pass

    def empty(self) -> None:
        self._content = list[ItemWrapper]()
        self.updateView()
