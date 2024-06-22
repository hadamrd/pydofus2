from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalPlusLookInformations import (
        CharacterMinimalPlusLookInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.FightPhase import FightPhase
    from pydofus2.com.ankamagames.dofus.network.types.game.social.fight.SocialFightInfo import SocialFightInfo


class SocialFight(NetworkMessage):
    socialFightInfo: "SocialFightInfo"
    attackers: list["CharacterMinimalPlusLookInformations"]
    defenders: list["CharacterMinimalPlusLookInformations"]
    phase: "FightPhase"

    def init(
        self,
        socialFightInfo_: "SocialFightInfo",
        attackers_: list["CharacterMinimalPlusLookInformations"],
        defenders_: list["CharacterMinimalPlusLookInformations"],
        phase_: "FightPhase",
    ):
        self.socialFightInfo = socialFightInfo_
        self.attackers = attackers_
        self.defenders = defenders_
        self.phase = phase_

        super().__init__()
