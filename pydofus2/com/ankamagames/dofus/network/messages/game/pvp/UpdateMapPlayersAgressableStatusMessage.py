from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.pvp.AgressableStatusMessage import \
        AgressableStatusMessage
    

class UpdateMapPlayersAgressableStatusMessage(NetworkMessage):
    playerAvAMessages: list['AgressableStatusMessage']
    def init(self, playerAvAMessages_: list['AgressableStatusMessage']):
        self.playerAvAMessages = playerAvAMessages_
        
        super().__init__()
    