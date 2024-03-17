from pydofus2.com.ankamagames.dofus.network.types.game.surrender.SurrenderRefused import \
    SurrenderRefused


class SurrenderRefusedBeforeTurn(SurrenderRefused):
    minTurnForSurrender: int
    def init(self, minTurnForSurrender_: int):
        self.minTurnForSurrender = minTurnForSurrender_
        
        super().init()
    