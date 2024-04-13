from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class Shortcut(NetworkMessage):
    slot: int

    def init(self, slot_: int):
        self.slot = slot_

        super().__init__()
