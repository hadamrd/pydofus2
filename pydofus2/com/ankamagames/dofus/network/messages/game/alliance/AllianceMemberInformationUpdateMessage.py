from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.alliance.AllianceMemberInfo import \
        AllianceMemberInfo


class AllianceMemberInformationUpdateMessage(NetworkMessage):
    member: "AllianceMemberInfo"

    def init(self, member_: "AllianceMemberInfo"):
        self.member = member_

        super().__init__()
