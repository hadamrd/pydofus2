from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
        GameRolePlayActorInformations
    

class GameRolePlayShowActorMessage(NetworkMessage):
    informations: 'GameRolePlayActorInformations'
    def init(self, informations_: 'GameRolePlayActorInformations'):
        self.informations = informations_
        
        super().__init__()
    