from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobBookSubscription import (
        JobBookSubscription,
    )


class JobBookSubscriptionMessage(NetworkMessage):
    subscriptions: list["JobBookSubscription"]

    def init(self, subscriptions_: list["JobBookSubscription"]):
        self.subscriptions = subscriptions_

        super().__init__()
