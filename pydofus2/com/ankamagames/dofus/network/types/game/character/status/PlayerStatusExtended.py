from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import PlayerStatus


class PlayerStatusExtended(PlayerStatus):
    message: str

    def init(self, message_: str, statusId_: int):
        self.message = message_

        super().init(statusId_)
