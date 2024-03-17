from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.alliance.recruitment.AllianceRecruitmentInformation import \
        AllianceRecruitmentInformation
    

class AllianceRecruitmentInformationMessage(NetworkMessage):
    recruitmentData: 'AllianceRecruitmentInformation'
    def init(self, recruitmentData_: 'AllianceRecruitmentInformation'):
        self.recruitmentData = recruitmentData_
        
        super().__init__()
    