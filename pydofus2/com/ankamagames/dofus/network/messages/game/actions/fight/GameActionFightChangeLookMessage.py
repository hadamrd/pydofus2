from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import \
    AbstractGameActionMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook


class GameActionFightChangeLookMessage(AbstractGameActionMessage):
    targetId: int
    entityLook: "EntityLook"

    def init(self, targetId_: int, entityLook_: "EntityLook", actionId_: int, sourceId_: int):
        self.targetId = targetId_
        self.entityLook = entityLook_

        super().init(actionId_, sourceId_)
