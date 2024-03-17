from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.guild.logbook.GuildLogbookEntryBasicInformation import \
    GuildLogbookEntryBasicInformation

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.rank.RankMinimalInformation import \
        RankMinimalInformation
    

class GuildRankActivity(GuildLogbookEntryBasicInformation):
    rankActivityType: int
    guildRankMinimalInfos: 'RankMinimalInformation'
    def init(self, rankActivityType_: int, guildRankMinimalInfos_: 'RankMinimalInformation', id_: int, date_: int):
        self.rankActivityType = rankActivityType_
        self.guildRankMinimalInfos = guildRankMinimalInfos_
        
        super().init(id_, date_)
    