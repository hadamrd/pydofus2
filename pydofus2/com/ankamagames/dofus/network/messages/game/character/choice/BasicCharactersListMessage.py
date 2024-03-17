from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.CharacterBaseInformations import \
        CharacterBaseInformations
    

class BasicCharactersListMessage(NetworkMessage):
    characters: list['CharacterBaseInformations']
    def init(self, characters_: list['CharacterBaseInformations']):
        self.characters = characters_
        
        super().__init__()
    