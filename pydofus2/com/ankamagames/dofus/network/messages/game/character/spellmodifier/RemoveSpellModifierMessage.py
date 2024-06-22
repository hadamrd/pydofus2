from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class RemoveSpellModifierMessage(NetworkMessage):
    actorId: int
    actionType: int
    modifierType: int
    spellId: int

    def init(self, actorId_: int, actionType_: int, modifierType_: int, spellId_: int):
        self.actorId = actorId_
        self.actionType = actionType_
        self.modifierType = modifierType_
        self.spellId = spellId_

        super().__init__()
