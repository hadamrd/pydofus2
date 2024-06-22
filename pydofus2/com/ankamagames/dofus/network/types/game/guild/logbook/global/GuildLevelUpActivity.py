from pydofus2.com.ankamagames.dofus.network.types.game.guild.logbook.GuildLogbookEntryBasicInformation import (
    GuildLogbookEntryBasicInformation,
)


class GuildLevelUpActivity(GuildLogbookEntryBasicInformation):
    newGuildLevel: int

    def init(self, newGuildLevel_: int, id_: int, date_: int):
        self.newGuildLevel = newGuildLevel_

        super().init(id_, date_)
