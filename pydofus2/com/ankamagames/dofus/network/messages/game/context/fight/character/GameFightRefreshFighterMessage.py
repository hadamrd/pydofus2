from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import \
        GameContextActorInformations
    

class GameFightRefreshFighterMessage(NetworkMessage):
    informations: 'GameContextActorInformations'
    def init(self, informations_: 'GameContextActorInformations'):
        self.informations = informations_
        
        super().__init__()
    