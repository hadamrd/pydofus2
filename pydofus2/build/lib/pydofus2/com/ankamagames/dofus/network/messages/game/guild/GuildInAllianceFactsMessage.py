from pydofus2.com.ankamagames.dofus.network.messages.game.guild.GuildFactsMessage import GuildFactsMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicNamedAllianceInformations import BasicNamedAllianceInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.social.GuildFactSheetInformations import GuildFactSheetInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalGuildPublicInformations import CharacterMinimalGuildPublicInformations
    


class GuildInAllianceFactsMessage(GuildFactsMessage):
    allianceInfos:'BasicNamedAllianceInformations'
    

    def init(self, allianceInfos_:'BasicNamedAllianceInformations', infos_:'GuildFactSheetInformations', creationDate_:int, nbTaxCollectors_:int, members_:list['CharacterMinimalGuildPublicInformations']):
        self.allianceInfos = allianceInfos_
        
        super().init(infos_, creationDate_, nbTaxCollectors_, members_)
    