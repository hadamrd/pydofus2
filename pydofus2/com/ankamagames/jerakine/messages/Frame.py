from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.messages.MessageHandler import MessageHandler
from pydofus2.com.ankamagames.jerakine.utils.misc.Priotizable import Prioritizable


class Frame(MessageHandler, Prioritizable):
    def process(self, msg: Message) -> bool:
        raise NotImplementedError("This method must be overriden")

    def pushed(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    def pulled(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __lt__(self, other: "Frame") -> bool:
        return self.priority.value > other.priority.value
