from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import KnownJobWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobBookSubscribeRequestAction import (
    JobBookSubscribeRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterContactLookRequestAction import (
    JobCrafterContactLookRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterDirectoryDefineSettingsAction import (
    JobCrafterDirectoryDefineSettingsAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterDirectoryListRequestAction import (
    JobCrafterDirectoryListRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.enums.SocialContactCategoryEnum import SocialContactCategoryEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobBookSubscriptionMessage import (
    JobBookSubscriptionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectoryDefineSettingsMessage import (
    JobCrafterDirectoryDefineSettingsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectoryListRequestMessage import (
    JobCrafterDirectoryListRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectorySettingsMessage import (
    JobCrafterDirectorySettingsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobDescriptionMessage import (
    JobDescriptionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceMultiUpdateMessage import (
    JobExperienceMultiUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceOtherPlayerUpdateMessage import (
    JobExperienceOtherPlayerUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceUpdateMessage import (
    JobExperienceUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobLevelUpMessage import JobLevelUpMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkJobIndexMessage import (
    ExchangeStartOkJobIndexMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.JobBookSubscribeRequestMessage import (
    JobBookSubscribeRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.social.ContactLookRequestByIdMessage import (
    ContactLookRequestByIdMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobBookSubscription import JobBookSubscription
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectorySettings import (
    JobCrafterDirectorySettings,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobDescription import JobDescription
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobExperience import JobExperience
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

logger = Logger("Dofus2")


class JobsFrame(Frame):

    # _jobCrafterDirectoryListDialogFrame: JobCrafterDirectoryListDialogFrame

    _settings: dict

    def __init__(self):
        self._settings = dict()
        super().__init__()

    def updateJobExperience(self, je: JobExperience) -> None:
        kj: KnownJobWrapper = PlayedCharacterManager().jobs[je.jobId]
        if not kj:
            kj = KnownJobWrapper.create(je.jobId)
            PlayedCharacterManager().jobs[je.jobId] = kj
        kj.jobLevel = je.jobLevel
        kj.jobXP = je.jobXP
        kj.jobXpLevelFloor = je.jobXpLevelFloor
        kj.jobXpNextLevelFloor = je.jobXpNextLevelFloor

    def createCrafterDirectorySettings(self, settings: JobCrafterDirectorySettings) -> object:
        obj = {}
        obj["jobId"] = settings.jobId
        obj["minLevel"] = settings.minLevel
        obj["free"] = settings.free
        return obj

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def settings(self) -> list:
        return self._settings

    def pushed(self) -> bool:
        # self._jobCrafterDirectoryListDialogFrame = JobCrafterDirectoryListDialogFrame()
        return True

    def process(self, msg: Message) -> bool:
        jdmsg: JobDescriptionMessage = None
        jcdsmsg: JobCrafterDirectorySettingsMessage = None
        jcddsa: JobCrafterDirectoryDefineSettingsAction = None
        jcddsmsg: JobCrafterDirectoryDefineSettingsMessage = None
        jeopumsg: JobExperienceOtherPlayerUpdateMessage = None
        jeumsg: JobExperienceUpdateMessage = None
        jemumsg: JobExperienceMultiUpdateMessage = None
        jlumsg: JobLevelUpMessage = None
        jobsNumber: int = 0
        lastJobLevel: int = 0
        jobName: str = None
        kj: KnownJobWrapper = None
        newJobLevel: int = 0
        podsBonus: int = 0
        levelUpTextMessage: str = None
        jbsra: JobBookSubscribeRequestAction = None
        exmsg: JobBookSubscribeRequestMessage = None
        jbsmsg: JobBookSubscriptionMessage = None
        jobSub: JobBookSubscription = None
        allTheSame: bool = False
        subscriptionState: bool = False
        text: str = None
        jcdlra: JobCrafterDirectoryListRequestAction = None
        jcdlrmsg: JobCrafterDirectoryListRequestMessage = None
        jcclra: JobCrafterContactLookRequestAction = None
        esokimsg: ExchangeStartOkJobIndexMessage = None
        array: list = None
        jd: JobDescription = None
        kj2: KnownJobWrapper = None
        setting: JobCrafterDirectorySettings = None
        je: JobExperience = None
        kjw: KnownJobWrapper = None
        job: Job = None
        clrbimsg: ContactLookRequestByIdMessage = None
        esojijob: int = 0
        if isinstance(msg, JobDescriptionMessage):
            jdmsg = msg
            PlayedCharacterManager().jobs = dict()
            for jd in jdmsg.jobsDescription:
                if jd:
                    kj2 = KnownJobWrapper.create(jd.jobId)
                    kj2.jobDescription = jd
                    PlayedCharacterManager().jobs[jd.jobId] = kj2
            return True
        if isinstance(msg, JobCrafterDirectorySettingsMessage):
            jcdsmsg = msg
            for setting in jcdsmsg.craftersSettings:
                self._settings[setting.jobId] = self.createCrafterDirectorySettings(setting)
            return True
        if isinstance(msg, JobCrafterDirectoryDefineSettingsAction):
            jcddsa = msg
            jcddsmsg = JobCrafterDirectoryDefineSettingsMessage()
            jcddsmsg.init(jcddsa.settings)
            ConnectionsHandler()._conn.send(jcddsmsg)
            return True
        if isinstance(msg, JobExperienceOtherPlayerUpdateMessage):
            return True
        if isinstance(msg, JobExperienceUpdateMessage):
            jeumsg = msg
            self.updateJobExperience(jeumsg.experiencesUpdate)
            return True
        if isinstance(msg, JobExperienceMultiUpdateMessage):
            jemumsg = msg
            for je in jemumsg.experiencesUpdate:
                self.updateJobExperience(je)
            return True
        if isinstance(msg, JobLevelUpMessage):
            jlumsg = msg
            jobsNumber = PlayedCharacterManager().jobsNumber()
            lastJobLevel = PlayedCharacterManager().jobsLevel()
            lastJobLevel -= jobsNumber
            jobName = Job.getJobById(jlumsg.jobsDescription.jobId).name
            kj = PlayedCharacterManager().jobs[jlumsg.jobsDescription.jobId]
            kj.jobDescription = jlumsg.jobsDescription
            kj.jobLevel = jlumsg.newLevel
            newJobLevel = PlayedCharacterManager().jobsLevel()
            newJobLevel -= jobsNumber
            podsBonus = self.jobLevelupPodsBonus(newJobLevel, lastJobLevel)
            levelUpTextMessage = I18n.getUiText("ui.craft.newJobLevel", [jobName, jlumsg.newLevel, podsBonus])
            logger.info(levelUpTextMessage)
            return True
        if isinstance(msg, JobBookSubscribeRequestAction):
            jbsra = msg
            exmsg = JobBookSubscribeRequestMessage()
            exmsg.init(jbsra.jobIds)
            ConnectionsHandler()._conn.send(exmsg)
            return True
        if isinstance(msg, JobBookSubscriptionMessage):
            jbsmsg = msg
            for jobSub in jbsmsg.subscriptions:
                PlayedCharacterManager().jobs[jobSub.jobId].jobBookSubscriber = jobSub.subscribed
            allTheSame = True
            subscriptionState = jbsmsg.subscriptions[0].subscribed
            for kjw in PlayedCharacterManager().jobs:
                if kjw.jobBookSubscriber != subscriptionState:
                    allTheSame = False
            if not allTheSame:
                for jobSub in jbsmsg.subscriptions:
                    job = Job.getJobById(jobSub.jobId)
                    if jobSub.subscribed:
                        text = I18n.getUiText("ui.craft.referenceAdd", [job.name])
                    else:
                        text = I18n.getUiText("ui.craft.referenceRemove", [job.name])
            else:
                if subscriptionState:
                    text = I18n.getUiText("ui.craft.referenceAddAll")
                else:
                    text = I18n.getUiText("ui.craft.referenceRemoveAll")
            logger.info(text)
            return True
        if isinstance(msg, JobCrafterDirectoryListRequestAction):
            jcdlra = msg
            jcdlrmsg = JobCrafterDirectoryListRequestMessage()
            jcdlrmsg.initJobCrafterDirectoryListRequestMessage(jcdlra.jobId)
            ConnectionsHandler()._conn.send(jcdlrmsg)
            return True
        if isinstance(msg, JobCrafterContactLookRequestAction):
            jcclra = msg
            if jcclra.crafterId == PlayedCharacterManager().id:
                pass
            else:
                clrbimsg = ContactLookRequestByIdMessage()
                clrbimsg.init(0, SocialContactCategoryEnum.SOCIAL_CONTACT_CRAFTER, jcclra.crafterId)
                ConnectionsHandler()._conn.send(clrbimsg)
            return True
        if isinstance(msg, ExchangeStartOkJobIndexMessage):
            esokimsg = msg
            array = list()
            for esojijob in esokimsg.jobs:
                array.append(esojijob)
            Kernel().worker.addFrame(self._jobCrafterDirectoryListDialogFrame)
            return True
        else:
            return False

    def pulled(self) -> bool:
        return True

    def jobLevelupPodsBonus(self, newJobsLevel: int, lastJobsLevel: int) -> int:
        paramsNewJob: dict = dict()
        paramsLastJob: dict = dict()
        paramsNewJob["sum_of_jobs_earned_levels"] = newJobsLevel
        paramsLastJob["sum_of_jobs_earned_levels"] = lastJobsLevel
        return 0
        # return (LuaScriptManager().executeLuaFormula(LuaFormulasEnum.JOBLEVELUP_PODSBONUS, paramsNewJob)) - (
        #     LuaScriptManager().executeLuaFormula(LuaFormulasEnum.JOBLEVELUP_PODSBONUS, paramsLastJob)
        # )
