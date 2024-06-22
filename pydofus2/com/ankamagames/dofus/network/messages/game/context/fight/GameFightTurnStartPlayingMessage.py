from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameFightTurnStartPlayingMessage(NetworkMessage):
    def init(self):

        super().__init__()
