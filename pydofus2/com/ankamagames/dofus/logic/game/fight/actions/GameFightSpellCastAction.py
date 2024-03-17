import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class GameFightSpellCastAction(AbstractAction, Action):

    spellId: int
    slot: int

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, spellId: int, slot: int) -> "GameFightSpellCastAction":
        a: GameFightSpellCastAction = GameFightSpellCastAction(sys.argv[1:])
        a.spellId = spellId
        a.slot = slot
        return a
