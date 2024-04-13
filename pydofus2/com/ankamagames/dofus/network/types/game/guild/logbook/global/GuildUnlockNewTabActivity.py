from pydofus2.com.ankamagames.dofus.network.types.game.guild.logbook.GuildLogbookEntryBasicInformation import (
    GuildLogbookEntryBasicInformation,
)


class GuildUnlockNewTabActivity(GuildLogbookEntryBasicInformation):
    def init(self, id_: int, date_: int):

        super().init(id_, date_)
