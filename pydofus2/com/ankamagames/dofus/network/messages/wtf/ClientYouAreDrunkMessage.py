from pydofus2.com.ankamagames.dofus.network.messages.debug.DebugInClientMessage import DebugInClientMessage


class ClientYouAreDrunkMessage(DebugInClientMessage):
    def init(self, level_: int, message_: str):

        super().init(level_, message_)
