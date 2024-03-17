from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class KohAllianceRoleMembers(NetworkMessage):
    memberCount: int
    roleAvAId: int
    def init(self, memberCount_: int, roleAvAId_: int):
        self.memberCount = memberCount_
        self.roleAvAId = roleAvAId_
        
        super().__init__()
    