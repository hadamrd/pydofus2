from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.Contribution import \
        Contribution


class GuildChestTabContributionsMessage(NetworkMessage):
    contributions: list["Contribution"]

    def init(self, contributions_: list["Contribution"]):
        self.contributions = contributions_

        super().__init__()
