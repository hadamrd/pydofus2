from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class GameRolePlayArenaSwitchToFightServerMessage(NetworkMessage):
    address: str
    ports: list[int]
    token: str

    def init(self, address_: str, ports_: list[int], token_: str):
        self.address = address_
        self.ports = ports_
        self.token = token_

        super().__init__()
