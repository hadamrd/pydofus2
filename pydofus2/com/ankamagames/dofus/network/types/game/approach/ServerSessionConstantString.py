from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstant import ServerSessionConstant


class ServerSessionConstantString(ServerSessionConstant):
    value: str

    def init(self, value_: str, id_: int):
        self.value = value_

        super().init(id_)
