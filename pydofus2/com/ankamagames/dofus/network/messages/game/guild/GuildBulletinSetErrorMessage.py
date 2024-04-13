from pydofus2.com.ankamagames.dofus.network.messages.game.social.SocialNoticeSetErrorMessage import (
    SocialNoticeSetErrorMessage,
)


class GuildBulletinSetErrorMessage(SocialNoticeSetErrorMessage):
    def init(self, reason_: int):

        super().init(reason_)
