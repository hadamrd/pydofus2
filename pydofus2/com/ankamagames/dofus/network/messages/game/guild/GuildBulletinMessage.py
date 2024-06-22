from pydofus2.com.ankamagames.dofus.network.messages.game.social.BulletinMessage import BulletinMessage


class GuildBulletinMessage(BulletinMessage):
    def init(self, content_: str, timestamp_: int, memberId_: int, memberName_: str):

        super().init(content_, timestamp_, memberId_, memberName_)
