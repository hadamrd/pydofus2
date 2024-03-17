from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.friend.IgnoredInformations import \
    IgnoredInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import \
        AccountTagInformation
    

class IgnoredOnlineInformations(IgnoredInformations):
    playerId: int
    playerName: str
    breed: int
    sex: bool
    def init(self, playerId_: int, playerName_: str, breed_: int, sex_: bool, accountId_: int, accountTag_: 'AccountTagInformation'):
        self.playerId = playerId_
        self.playerName = playerName_
        self.breed = breed_
        self.sex = sex_
        
        super().init(accountId_, accountTag_)
    