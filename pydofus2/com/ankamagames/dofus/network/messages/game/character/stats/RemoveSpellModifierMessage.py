from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class RemoveSpellModifierMessage(NetworkMessage):
    actorId: int
    modificationType: int
    spellId: int

    def init(self, actorId_: int, modificationType_: int, spellId_: int):
        self.actorId = actorId_
        self.modificationType = modificationType_
        self.spellId = spellId_

        super().__init__()
