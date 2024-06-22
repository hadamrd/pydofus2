from pydofus2.com.ankamagames.dofus.network.messages.game.context.ShowCellMessage import ShowCellMessage


class ShowCellSpectatorMessage(ShowCellMessage):
    playerName: str

    def init(self, playerName_: str, sourceId_: int, cellId_: int):
        self.playerName = playerName_

        super().init(sourceId_, cellId_)
