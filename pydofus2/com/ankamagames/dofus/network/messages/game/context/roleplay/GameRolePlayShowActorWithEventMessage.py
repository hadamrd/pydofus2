from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.GameRolePlayShowActorMessage import (
    GameRolePlayShowActorMessage,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import (
        GameRolePlayActorInformations,
    )


class GameRolePlayShowActorWithEventMessage(GameRolePlayShowActorMessage):
    actorEventId: int

    def init(self, actorEventId_: int, informations_: "GameRolePlayActorInformations"):
        self.actorEventId = actorEventId_

        super().init(informations_)
