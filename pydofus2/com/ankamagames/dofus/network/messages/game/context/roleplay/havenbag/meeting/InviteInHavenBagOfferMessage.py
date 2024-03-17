from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import \
        CharacterMinimalInformations
    

class InviteInHavenBagOfferMessage(NetworkMessage):
    hostInformations: 'CharacterMinimalInformations'
    timeLeftBeforeCancel: int
    def init(self, hostInformations_: 'CharacterMinimalInformations', timeLeftBeforeCancel_: int):
        self.hostInformations = hostInformations_
        self.timeLeftBeforeCancel = timeLeftBeforeCancel_
        
        super().__init__()
    