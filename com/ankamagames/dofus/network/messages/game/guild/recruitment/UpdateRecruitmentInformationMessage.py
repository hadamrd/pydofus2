from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from com.ankamagames.dofus.network.types.game.guild.recruitment.GuildRecruitmentInformation import GuildRecruitmentInformation


class UpdateRecruitmentInformationMessage(INetworkMessage):
    protocolId = 3169
    recruitmentData:GuildRecruitmentInformation
    
    
