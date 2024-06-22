from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEffectTriggerCount import (
        GameFightEffectTriggerCount,
    )


class GameActionUpdateEffectTriggerCountMessage(NetworkMessage):
    targetIds: list["GameFightEffectTriggerCount"]

    def init(self, targetIds_: list["GameFightEffectTriggerCount"]):
        self.targetIds = targetIds_

        super().__init__()
