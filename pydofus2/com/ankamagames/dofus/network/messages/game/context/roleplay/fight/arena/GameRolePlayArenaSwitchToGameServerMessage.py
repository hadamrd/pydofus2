from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameRolePlayArenaSwitchToGameServerMessage(NetworkMessage):
    validToken: bool
    token: str
    homeServerId: int

    def init(self, validToken_: bool, token_: str, homeServerId_: int):
        self.validToken = validToken_
        self.token = token_
        self.homeServerId = homeServerId_

        super().__init__()
