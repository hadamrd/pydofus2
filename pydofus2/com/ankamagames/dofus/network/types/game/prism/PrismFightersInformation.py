from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import \
        CharacterMinimalPlusLookInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.fight.ProtectedEntityWaitingForHelpInfo import \
        ProtectedEntityWaitingForHelpInfo
    

class PrismFightersInformation(NetworkMessage):
    subAreaId: int
    waitingForHelpInfo: 'ProtectedEntityWaitingForHelpInfo'
    allyCharactersInformations: list['CharacterMinimalPlusLookInformations']
    enemyCharactersInformations: list['CharacterMinimalPlusLookInformations']
    def init(self, subAreaId_: int, waitingForHelpInfo_: 'ProtectedEntityWaitingForHelpInfo', allyCharactersInformations_: list['CharacterMinimalPlusLookInformations'], enemyCharactersInformations_: list['CharacterMinimalPlusLookInformations']):
        self.subAreaId = subAreaId_
        self.waitingForHelpInfo = waitingForHelpInfo_
        self.allyCharactersInformations = allyCharactersInformations_
        self.enemyCharactersInformations = enemyCharactersInformations_
        
        super().__init__()
    