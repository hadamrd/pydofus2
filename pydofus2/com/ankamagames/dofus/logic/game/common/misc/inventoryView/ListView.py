from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IInventoryView import IInventoryView


class ListView(IInventoryView):
    _view: list[ItemWrapper]

    def __init__(self):
        self._view = list[ItemWrapper]()
        super().__init__()

    @property
    def name(self) -> str:
        raise Exception("get name() is abstract method, it should be implemented")

    def initialize(self, items: list[ItemWrapper]) -> None:
        self._view.clear()
        for item in items:
            self._view.append(item)
        self.updateView()

    @property
    def content(self) -> list[ItemWrapper]:
        return self._view

    def addItem(self, item: ItemWrapper, invisible: int, needUpdateView: bool = True) -> None:
        self._view.append(item)

    def removeItem(self, item: ItemWrapper, invisible: int) -> None:
        if item not in self._view:
            raise Exception(
                "Demande de suppression d'un item (id "
                + str(item.objectUID)
                + ") qui n'existe pas dans la vue "
                + self.name
            )
        self._view.remove(item)

    def modifyItem(self, item: ItemWrapper, oldItem: ItemWrapper, invisible: int) -> None:
        if item not in self._view:
            raise Exception(
                "Demande de modification d'un item (id "
                + str(item.objectUID)
                + ") qui n'existe pas dans la vue "
                + self.name
            )
        idx = self._view.index(item)
        self._view[idx] = item

    def isListening(self, item: ItemWrapper) -> bool:
        raise Exception("isListening() is abstract method, it should be implemented")

    def updateView(self) -> None:
        raise Exception("updateView() is abstract method, it should be implemented")

    def empty(self) -> None:
        self._view = list[ItemWrapper]()
        self.updateView()
