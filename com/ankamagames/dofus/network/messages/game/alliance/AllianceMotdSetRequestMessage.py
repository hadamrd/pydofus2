from com.ankamagames.dofus.network.messages.game.social.SocialNoticeSetRequestMessage import SocialNoticeSetRequestMessage


class AllianceMotdSetRequestMessage(SocialNoticeSetRequestMessage):
    content:str
    

    def init(self, content:str):
        self.content = content
        
        super().__init__()
    
    