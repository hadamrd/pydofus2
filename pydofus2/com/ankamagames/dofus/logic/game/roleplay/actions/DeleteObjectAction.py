import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class DeleteObjectAction(AbstractAction, Action):

    objectUID: int

    quantity: int

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, objectUID: int, quantity: int) -> "DeleteObjectAction":
        a: DeleteObjectAction = DeleteObjectAction(sys.argv[1:])
        a.objectUID = objectUID
        a.quantity = quantity
        return a
