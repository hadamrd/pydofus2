from com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


class CharacterExperienceGainMessage(INetworkMessage):
    protocolId = 4524
    experienceCharacter:int
    experienceMount:int
    experienceGuild:int
    experienceIncarnation:int
    
    
