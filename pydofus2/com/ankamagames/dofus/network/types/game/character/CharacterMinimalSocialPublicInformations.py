from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import (
    CharacterMinimalInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.guild.RankPublicInformation import RankPublicInformation


class CharacterMinimalSocialPublicInformations(CharacterMinimalInformations):
    rank: "RankPublicInformation"

    def init(self, rank_: "RankPublicInformation", level_: int, name_: str, id_: int):
        self.rank = rank_

        super().init(level_, name_, id_)
