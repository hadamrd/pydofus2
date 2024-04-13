from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameRolePlayArenaRegisterMessage(NetworkMessage):
    arenaType: int

    def init(self, arenaType_: int):
        self.arenaType = arenaType_

        super().__init__()
