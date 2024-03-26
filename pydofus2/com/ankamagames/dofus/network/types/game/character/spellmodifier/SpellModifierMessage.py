from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class SpellModifierMessage(NetworkMessage):
    spellId: int
    actionType: int
    modifierType: int
    context: int
    equipment: int

    def init(self, spellId_: int, actionType_: int, modifierType_: int, context_: int, equipment_: int):
        self.spellId = spellId_
        self.actionType = actionType_
        self.modifierType = modifierType_
        self.context = context_
        self.equipment = equipment_

        super().__init__()
