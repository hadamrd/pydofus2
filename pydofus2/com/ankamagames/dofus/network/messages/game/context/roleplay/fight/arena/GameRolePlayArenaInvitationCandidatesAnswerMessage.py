from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.fight.arena.LeagueFriendInformations import (
        LeagueFriendInformations,
    )


class GameRolePlayArenaInvitationCandidatesAnswerMessage(NetworkMessage):
    candidates: list["LeagueFriendInformations"]

    def init(self, candidates_: list["LeagueFriendInformations"]):
        self.candidates = candidates_

        super().__init__()
