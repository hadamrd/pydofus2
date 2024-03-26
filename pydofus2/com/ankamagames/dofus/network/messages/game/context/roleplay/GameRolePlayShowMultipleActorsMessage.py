from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayActorInformations import \
        GameRolePlayActorInformations


class GameRolePlayShowMultipleActorsMessage(NetworkMessage):
    informationsList: list["GameRolePlayActorInformations"]

    def init(self, informationsList_: list["GameRolePlayActorInformations"]):
        self.informationsList = informationsList_

        super().__init__()
