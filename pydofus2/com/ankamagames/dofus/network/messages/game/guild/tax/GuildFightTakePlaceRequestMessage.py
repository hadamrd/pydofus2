from pydofus2.com.ankamagames.dofus.network.messages.game.guild.tax.GuildFightJoinRequestMessage import (
    GuildFightJoinRequestMessage,
)


class GuildFightTakePlaceRequestMessage(GuildFightJoinRequestMessage):
    replacedCharacterId: int

    def init(self, replacedCharacterId_: int, taxCollectorId_: int):
        self.replacedCharacterId = replacedCharacterId_

        super().init(taxCollectorId_)
