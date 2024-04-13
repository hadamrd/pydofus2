from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.QuestActiveInformations import (
        QuestActiveInformations,
    )


class QuestStepInfoMessage(NetworkMessage):
    infos: "QuestActiveInformations"

    def init(self, infos_: "QuestActiveInformations"):
        self.infos = infos_

        super().__init__()
