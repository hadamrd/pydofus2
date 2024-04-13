from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.guild.tax.TaxCollectorComplementaryInformations import (
    TaxCollectorComplementaryInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicGuildInformations import (
        BasicGuildInformations,
    )


class TaxCollectorGuildInformations(TaxCollectorComplementaryInformations):
    guild: "BasicGuildInformations"

    def init(self, guild_: "BasicGuildInformations"):
        self.guild = guild_

        super().init()
