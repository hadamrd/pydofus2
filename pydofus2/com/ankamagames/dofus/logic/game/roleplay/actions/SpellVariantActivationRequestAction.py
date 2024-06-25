import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class SpellVariantActivationRequestAction(AbstractAction, Action):

    spellId: int

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, spellId: int) -> "SpellVariantActivationRequestAction":
        a = cls(sys.argv[1:])
        a.spellId = spellId
        return a
