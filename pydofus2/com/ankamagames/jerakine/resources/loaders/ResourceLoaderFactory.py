from pydofus2.com.ankamagames.jerakine import JerakineConstants
from pydofus2.com.ankamagames.jerakine.resources.loaders.impl.ParallelResourceLoader import ParallelResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.loaders.impl.SingleResourceLoader import SingleResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType


class ResourceLoaderFactory:
    @staticmethod
    def getLoader(type):
        if type == ResourceLoaderType.PARALLEL_LOADER:
            return ParallelResourceLoader(JerakineConstants.MAX_PARALLEL_LOADINGS)
        elif type == ResourceLoaderType.SERIAL_LOADER:
            return ParallelResourceLoader(1)
        elif type == ResourceLoaderType.SINGLE_LOADER:
            return SingleResourceLoader()
        else:
            raise ValueError("Unknown loader type " + str(type) + ".")
