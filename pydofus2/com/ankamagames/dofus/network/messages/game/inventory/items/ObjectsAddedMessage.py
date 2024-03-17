from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItem import \
        ObjectItem
    

class ObjectsAddedMessage(NetworkMessage):
    object: list['ObjectItem']
    def init(self, object_: list['ObjectItem']):
        self.object = object_
        
        super().__init__()
    