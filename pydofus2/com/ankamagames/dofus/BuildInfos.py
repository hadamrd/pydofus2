import pydofus2.com.ankamagames.dofus.settings as settings
from pydofus2.com.ankamagames.dofus.misc.BuildTypeParser import BuildTypeParser
from pydofus2.com.ankamagames.dofus.network.enums.BuildTypeEnum import \
    BuildTypeEnum
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.Version import Version


class BuildInfos(metaclass=Singleton):
    with open(settings.GAME_VERSION_PATH, "r") as fp:
        VERSION: Version = Version(fp.read().strip(), BuildTypeEnum.RELEASE.value)

    BUILD_DATE: str = "01/Jan/1970"

    def __init__(self):
        super().__init__()

    @property
    def buildTypeName(self) -> str:
        return BuildTypeParser.getTypeName(self.VERSION.buildType)

    @property
    def BUILD_TYPE(self) -> int:
        return self.VERSION.buildType
