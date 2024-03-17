from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.IInventoryView import \
    IInventoryView
from pydofus2.com.ankamagames.dofus.network.enums.CharacterInventoryPositionEnum import \
    CharacterInventoryPositionEnum
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class RoleplayBuffView(IInventoryView):

    _content: list[ItemWrapper]

    def __init__(self):
        super().__init__()

    def initialize(self, items: list[ItemWrapper]) -> None:
        item: ItemWrapper = None
        self._content = list[ItemWrapper]()
        for item in items:
            if self.isListening(item):
                self.addItem(item, 0, False)
        self.updateView()

    @property
    def name(self) -> str:
        return "roleplayBuff"

    @property
    def content(self) -> list[ItemWrapper]:
        return self._content

    def addItem(self, item: ItemWrapper, invisible: int, needUpdateView: bool = True) -> None:
        self._content = [item] + self._content
        if needUpdateView:
            self.updateView()

    def removeItem(self, item: ItemWrapper, invisible: int) -> None:
        if item not in self.content:
            Logger().warn("L'item qui doit �tre supprim� n'est pas pr�sent dans la liste")
        self.content.remove(item)
        self.updateView()

    def modifyItem(self, item: ItemWrapper, oldItem: ItemWrapper, invisible: int) -> None:
        self.updateView()

    def isListening(self, item: ItemWrapper) -> bool:
        return (
            item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_MUTATION
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_BOOST_FOOD
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_FIRST_BONUS
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_SECOND_BONUS
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_FIRST_MALUS
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_SECOND_MALUS
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_ROLEPLAY_BUFFER
            or item.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_FOLLOWER
        )

    def updateView(self) -> None:
        pass

    def empty(self) -> None:
        self._content = list[ItemWrapper]()
        self.updateView()
