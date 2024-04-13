from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GuildApplicationPresenceMessage(NetworkMessage):
    isApplication: bool

    def init(self, isApplication_: bool):
        self.isApplication = isApplication_

        super().__init__()
