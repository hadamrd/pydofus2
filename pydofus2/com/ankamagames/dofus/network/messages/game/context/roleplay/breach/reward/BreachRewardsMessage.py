from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.breach.BreachReward import BreachReward


class BreachRewardsMessage(NetworkMessage):
    rewards: list["BreachReward"]

    def init(self, rewards_: list["BreachReward"]):
        self.rewards = rewards_

        super().__init__()
