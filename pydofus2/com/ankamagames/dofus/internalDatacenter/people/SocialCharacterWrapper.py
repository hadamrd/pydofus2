from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SocialCharacterWrapper(IDataCenter):
    def __init__(self, name: str, tag: str, accountId: int):
        super().__init__()
        self.name = name
        self.tag = tag
        self.accountId = accountId
        self.state = 0
        self.lastConnection = 0
        self.online = False
        self.e_category = 0
        self.playerId = 0
        self.playerName = ""
        self.breed = 0
        self.sex = 2
        self.level = 0
        self.alignmentSide = 0
        self.guildName = ""
        self.achievementPoints = 0
