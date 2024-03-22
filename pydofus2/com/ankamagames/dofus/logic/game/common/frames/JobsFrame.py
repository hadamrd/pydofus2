from prettytable import PrettyTable

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import \
    KnownJobWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobBookSubscribeRequestAction import \
    JobBookSubscribeRequestAction
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterContactLookRequestAction import \
    JobCrafterContactLookRequestAction
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterDirectoryDefineSettingsAction import \
    JobCrafterDirectoryDefineSettingsAction
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.craft.JobCrafterDirectoryListRequestAction import \
    JobCrafterDirectoryListRequestAction
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.utils.enums.LuaFormulasEnum import \
    LuaFormulasEnum
from pydofus2.com.ankamagames.dofus.misc.utils.LuaScriptManager import \
    LuaScriptManager
from pydofus2.com.ankamagames.dofus.network.enums.SocialContactCategoryEnum import \
    SocialContactCategoryEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobBookSubscriptionMessage import \
    JobBookSubscriptionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectoryDefineSettingsMessage import \
    JobCrafterDirectoryDefineSettingsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectoryListRequestMessage import \
    JobCrafterDirectoryListRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobCrafterDirectorySettingsMessage import \
    JobCrafterDirectorySettingsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobDescriptionMessage import \
    JobDescriptionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceMultiUpdateMessage import \
    JobExperienceMultiUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceOtherPlayerUpdateMessage import \
    JobExperienceOtherPlayerUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobExperienceUpdateMessage import \
    JobExperienceUpdateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.job.JobLevelUpMessage import \
    JobLevelUpMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartOkJobIndexMessage import \
    ExchangeStartOkJobIndexMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.JobBookSubscribeRequestMessage import \
    JobBookSubscribeRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.social.ContactLookRequestByIdMessage import \
    ContactLookRequestByIdMessage
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectorySettings import \
    JobCrafterDirectorySettings
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobExperience import \
    JobExperience
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class JobsFrame(Frame):
    _settings: dict

    def __init__(self):
        self._settings = dict()
        super().__init__()

    def updateJobExperience(self, je: JobExperience) -> None:
        kj: KnownJobWrapper = PlayedCharacterManager().jobs.get(je.jobId)
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

    def pulled(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:
        if isinstance(msg, JobDescriptionMessage):
            PlayedCharacterManager().jobs = dict()
            for jd in msg.jobsDescription:
                if jd:
                    kj2 = KnownJobWrapper.create(jd.jobId)
                    kj2.jobDescription = jd
                    PlayedCharacterManager().jobs[jd.jobId] = kj2
            return True

        if isinstance(msg, JobCrafterDirectorySettingsMessage):
            for setting in msg.craftersSettings:
                self._settings[setting.jobId] = self.createCrafterDirectorySettings(setting)
            return True

        if isinstance(msg, JobCrafterDirectoryDefineSettingsAction):
            jcddsmsg = JobCrafterDirectoryDefineSettingsMessage()
            jcddsmsg.init(msg.settings)
            ConnectionsHandler().send(jcddsmsg)
            return True

        if isinstance(msg, JobExperienceOtherPlayerUpdateMessage):
            return True

        if isinstance(msg, JobExperienceUpdateMessage):
            oldJobXp = PlayedCharacterManager().jobs[msg.experiencesUpdate.jobId].jobXP
            self.updateJobExperience(msg.experiencesUpdate)
            KernelEventsManager().send(KernelEvent.JobExperienceUpdate, oldJobXp, msg.experiencesUpdate)
            return True

        if isinstance(msg, JobExperienceMultiUpdateMessage):
            for je in msg.experiencesUpdate:
                self.updateJobExperience(je)
            table = PrettyTable()
            # Define the column headers
            table.field_names = ["Name", "Level"]
            # Iterate over the jobs and add a row for each job
            for job in PlayedCharacterManager().jobs.values():
                table.add_row([job.name, job.jobLevel])
            Logger().info(f"Player jobs:\n{table}")
            return True

        if isinstance(msg, JobLevelUpMessage):
            kj = PlayedCharacterManager().jobs[msg.jobsDescription.jobId]
            lastJobLevel = kj.jobLevel
            jobName = Job.getJobById(msg.jobsDescription.jobId).name
            kj.jobDescription = msg.jobsDescription
            kj.jobLevel = msg.newLevel
            podsBonus = self.jobLevelupPodsBonus(msg.newLevel, lastJobLevel)
            Logger().info(f"Job {jobName} leveled Up to {msg.newLevel} you gained {podsBonus} extra pods")
            KernelEventsManager().send(
                KernelEvent.JobLevelUp, msg.jobsDescription.jobId, jobName, lastJobLevel, msg.newLevel, podsBonus
            )
            return True

        if isinstance(msg, JobBookSubscribeRequestAction):
            exmsg = JobBookSubscribeRequestMessage()
            exmsg.init(msg.jobIds)
            ConnectionsHandler().send(exmsg)
            return True

        if isinstance(msg, JobBookSubscriptionMessage):
            for jobSub in msg.subscriptions:
                PlayedCharacterManager().jobs[jobSub.jobId].jobBookSubscriber = jobSub.subscribed
            allTheSame = True
            subscriptionState = msg.subscriptions[0].subscribed
            for kjw in PlayedCharacterManager().jobs:
                if kjw.jobBookSubscriber != subscriptionState:
                    allTheSame = False
            if not allTheSame:
                for jobSub in msg.subscriptions:
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
            Logger().info(text)
            return True

        if isinstance(msg, JobCrafterDirectoryListRequestAction):
            jcdlrmsg = JobCrafterDirectoryListRequestMessage()
            jcdlrmsg.init(msg.jobId)
            ConnectionsHandler().send(jcdlrmsg)
            return True

        if isinstance(msg, JobCrafterContactLookRequestAction):
            if msg.crafterId == PlayedCharacterManager().id:
                pass
            else:
                clrbimsg = ContactLookRequestByIdMessage()
                clrbimsg.init(0, SocialContactCategoryEnum.SOCIAL_CONTACT_CRAFTER, msg.crafterId)
                ConnectionsHandler().send(clrbimsg)
            return True

        if isinstance(msg, ExchangeStartOkJobIndexMessage):
            array = list()
            for esojijob in msg.jobs:
                array.append(esojijob)
            Kernel().worker.addFrame(self._jobCrafterDirectoryListDialogFrame)
            return True

        else:
            return False

    def jobLevelupPodsBonus(self, newJobsLevel: int, lastJobsLevel: int) -> int:
        paramsNewJob: dict = dict()
        paramsLastJob: dict = dict()
        paramsNewJob["sum_of_jobs_earned_levels"] = newJobsLevel
        paramsLastJob["sum_of_jobs_earned_levels"] = lastJobsLevel
        return LuaScriptManager().executeLuaFormula(
            LuaFormulasEnum.JOB_LEVEL_UP_PODS_BONUS, paramsNewJob
        ) - LuaScriptManager().executeLuaFormula(LuaFormulasEnum.JOB_LEVEL_UP_PODS_BONUS, paramsLastJob)
