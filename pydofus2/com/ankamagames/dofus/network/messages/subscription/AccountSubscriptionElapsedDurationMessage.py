from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class AccountSubscriptionElapsedDurationMessage(NetworkMessage):
    subscriptionElapsedDuration: int

    def init(self, subscriptionElapsedDuration_: int):
        self.subscriptionElapsedDuration = subscriptionElapsedDuration_

        super().__init__()
