from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.friend.AcquaintanceInformation import \
    AcquaintanceInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation
    from pydofus2.com.ankamagames.dofus.network.types.game.character.status.PlayerStatus import \
        PlayerStatus
    

class AcquaintanceOnlineInformation(AcquaintanceInformation):
    playerId: int
    playerName: str
    moodSmileyId: int
    status: 'PlayerStatus'
    def init(self, playerId_: int, playerName_: str, moodSmileyId_: int, status_: 'PlayerStatus', playerState_: int, accountId_: int, accountTag_: 'AccountTagInformation'):
        self.playerId = playerId_
        self.playerName = playerName_
        self.moodSmileyId = moodSmileyId_
        self.status = status_
        
        super().init(playerState_, accountId_, accountTag_)
    