from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ReloginTokenStatusMessage(NetworkMessage):
    validToken: bool
    token: str

    def init(self, validToken_: bool, token_: str):
        self.validToken = validToken_
        self.token = token_

        super().__init__()
