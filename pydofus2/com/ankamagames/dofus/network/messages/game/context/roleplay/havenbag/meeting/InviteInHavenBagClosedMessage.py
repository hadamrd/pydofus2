from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import \
        CharacterMinimalInformations
    

class InviteInHavenBagClosedMessage(NetworkMessage):
    hostInformations: 'CharacterMinimalInformations'
    def init(self, hostInformations_: 'CharacterMinimalInformations'):
        self.hostInformations = hostInformations_
        
        super().__init__()
    