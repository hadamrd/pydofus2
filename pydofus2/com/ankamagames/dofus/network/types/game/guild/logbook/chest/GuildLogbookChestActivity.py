from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.guild.logbook.GuildLogbookEntryBasicInformation import \
    GuildLogbookEntryBasicInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.ObjectItemNotInContainer import \
        ObjectItemNotInContainer
    

class GuildLogbookChestActivity(GuildLogbookEntryBasicInformation):
    playerId: int
    playerName: str
    eventType: int
    quantity: int
    object: 'ObjectItemNotInContainer'
    sourceTabId: int
    destinationTabId: int
    def init(self, playerId_: int, playerName_: str, eventType_: int, quantity_: int, object_: 'ObjectItemNotInContainer', sourceTabId_: int, destinationTabId_: int, id_: int, date_: int):
        self.playerId = playerId_
        self.playerName = playerName_
        self.eventType = eventType_
        self.quantity = quantity_
        self.object = object_
        self.sourceTabId = sourceTabId_
        self.destinationTabId = destinationTabId_
        
        super().init(id_, date_)
    