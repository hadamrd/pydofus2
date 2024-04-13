from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.messages.MessageHandler import MessageHandler


class IInteractive(EventsHandler, IEntity):
    @property
    def handler(self) -> MessageHandler:
        pass

    @property
    def useHandCursor(self) -> bool:
        pass

    @property
    def enabledInteractions(self) -> int:
        pass
