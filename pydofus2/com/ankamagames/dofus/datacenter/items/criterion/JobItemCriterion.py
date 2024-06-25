from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import KnownJobWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class JobItemCriterion(ItemCriterion, IDataCenter):

    VALUE_NOT_SPECIFIC_JOB: int = 4.294967295e9

    _jobId: int

    _jobsCount: int

    _jobLevel: int = -1

    def __init__(self, pCriterion: str):
        isValidfloat: bool = False
        _jobIdentifier: list = None
        super().__init__(pCriterion)
        arrayParams: list = str(self._criterionValueText).split(",")
        if arrayParams and len(arrayParams) > 0:
            if len(arrayParams) <= 2:
                isValidfloat = (int(arrayParams[0])) is not None and int(arrayParams[0]) > 0
                if isValidfloat:
                    self._jobId = int(arrayParams[0])
                    self._jobsCount = 1
                else:
                    _jobIdentifier = arrayParams[0].split("")
                    if _jobIdentifier[0] == "a":
                        self._jobId = self.VALUE_NOT_SPECIFIC_JOB
                        self._jobsCount = 1
                    elif _jobIdentifier[0] == "n":
                        self._jobId = self.VALUE_NOT_SPECIFIC_JOB
                        self._jobsCount = int(_jobIdentifier[1])
                    else:
                        self._jobId = 0
                        self._jobsCount = 0
                self._jobLevel = int(arrayParams[1])
        else:
            self._jobId = int(self._criterionValue)
            self._jobLevel = -1

    @property
    def isRespected(self) -> bool:
        knownJob: KnownJobWrapper = None
        knownJobCount: int = 0
        knownJobs: list = PlayedCharacterManager().jobs
        if self._jobsCount > 0:
            if self._jobId == self.VALUE_NOT_SPECIFIC_JOB:
                knownJobCount = 0
                for knownJob in knownJobs:
                    if knownJob:
                        if self._jobLevel == -1 or knownJob.jobLevel > self._jobLevel:
                            knownJobCount += 1
                        if knownJobCount >= self._jobsCount:
                            return True
            else:
                knownJob = knownJobs[self._jobId]
                if not knownJob:
                    return False
                if self._jobLevel == -1 or knownJob.jobLevel > self._jobLevel:
                    return True
        return False

    @property
    def text(self) -> str:
        job: Job = None
        readableCriterionRef: str = ""
        readableCriterionValue: str = ""
        readableCriterion: str = ""
        if self._jobsCount > 0:
            if self._jobsCount > 1 or self._jobId == self.VALUE_NOT_SPECIFIC_JOB:
                readableCriterionValue += PatternDecoder.combine(
                    I18n.getUiText("ui.criterion.atLeastSomeJobs", [self._jobsCount]),
                    "n",
                    self._jobsCount == 1,
                    self._jobsCount == 0,
                )
            else:
                job = Job.getJobById(self._jobId)
                if not job:
                    return readableCriterion
                readableCriterionValue += job.name
            optionalJobLevel: str = ""
            if self._jobLevel >= 0:
                optionalJobLevel = " " + I18n.getUiText("ui.common.short.level") + " " + str(self._jobLevel)
            if self._operator.text == ItemCriterionOperator.EQUAL:
                readableCriterion = readableCriterionValue + optionalJobLevel
            elif self._operator.text == ItemCriterionOperator.DIFFERENT:
                readableCriterion = I18n.getUiText("ui.common.dontBe") + readableCriterionValue + optionalJobLevel
            elif self._operator.text == ItemCriterionOperator.SUPERIOR:
                readableCriterionRef = " >"
                readableCriterion = readableCriterionValue + readableCriterionRef + optionalJobLevel
            elif self._operator.text == ItemCriterionOperator.INFERIOR:
                readableCriterionRef = " <"
                readableCriterion = readableCriterionValue + readableCriterionRef + optionalJobLevel
                return readableCriterion
        return ""

    def clone(self) -> IItemCriterion:
        return JobItemCriterion(self.basicText)
