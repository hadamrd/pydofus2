from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.character.GameFightShowFighterMessage import \
    GameFightShowFighterMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
        GameFightFighterInformations


class GameFightShowFighterRandomStaticPoseMessage(GameFightShowFighterMessage):
    def init(self, informations_: "GameFightFighterInformations"):

        super().init(informations_)
