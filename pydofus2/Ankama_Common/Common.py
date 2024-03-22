
from pydofus2.Ankama_Common.ui.items.RecipesFilterWrapper import \
    RecipesFilterWrapper
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class Common(metaclass=Singleton):
    
    def __init__(self) -> None:
        self._jobSearchOptions = dict[int, RecipesFilterWrapper]()
    
    def getJobSearchOptionsByJobId(self, id) -> RecipesFilterWrapper:
        return self._jobSearchOptions.get(id)
    
    def setJobSearchOptionsByJobId(self, filter: RecipesFilterWrapper):
        self._jobSearchOptions[filter.jobId] = filter
