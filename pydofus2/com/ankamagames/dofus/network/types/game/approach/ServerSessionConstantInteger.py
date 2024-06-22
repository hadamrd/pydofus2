from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstant import ServerSessionConstant


class ServerSessionConstantInteger(ServerSessionConstant):
    value: int

    def init(self, value_: int, id_: int):
        self.value = value_

        super().init(id_)
