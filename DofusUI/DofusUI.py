import sys

from PyQt5.QtWidgets import QApplication, QGraphicsView, QMainWindow
from Sprite import Sprite
from Stage import Stage
from StageShareManager import StageShareManager

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.atouin.rtypes.AtouinOptions import AtouinOptions
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.types.DofusOptions import DofusOptions
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.managers.OptionManager import OptionManager


class DofusUI(QMainWindow):
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DofusUI, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if self._initialized:
            return
        super(DofusUI, self).__init__(parent)
        self.setObjectName("sharedStage")
        self.setWindowTitle("DofusUI")
        self.stage = Stage(self)
        self.view = QGraphicsView(self.stage)
        self.view.setObjectName("stage main view")
        self.setCentralWidget(self.view)
        self._worldContainer = None
        self.initWorld()
        self.initStageManager()
        self.show()

    def setDisplayOptions(self, opt: DofusOptions):
        self.initWindow(opt.getOption("fullScreen"))
        self._doOptions = opt
        self._doOptions.addEventListener(PropertyChangeEvent.PROPERTY_CHANGED, self.onOptionChange)
        self._doOptions.setOption("flashQuality", self._doOptions.getOption("flashQuality"))
        self._doOptions.setOption("fullScreen", self._doOptions.getOption("fullScreen"))

    def initStageManager(self):
        StageShareManager().stage = self.stage
        StageShareManager().rootContainer = self

    def initWorld(self):
        self._worldContainer = Sprite()
        self.stage.addItem(self._worldContainer)

    def getWorldContainer(self) -> Sprite:
        return self._worldContainer

    def initOptions(self):
        OptionManager.reset()
        ao = AtouinOptions(DofusUI().getWorldContainer(), Kernel().worker)
        ao.setOption(
            "frustum",
            Frustum(
                LangManager().getIntEntry("config.atouin.frustum.marginLeft"),
                LangManager().getIntEntry("config.atouin.frustum.marginTop"),
                LangManager().getIntEntry("config.atouin.frustum.marginRight"),
                LangManager().getIntEntry("config.atouin.frustum.marginBottom"),
            ),
        )
        ao.setOption("mapsPath", LangManager().getEntry("config.atouin.path.maps"))
        ao.setOption("elementsIndexPath", LangManager().getEntry("config.atouin.path.elements"))
        ao.setOption("elementsPath", LangManager().getEntry("config.gfx.path.cellElement"))
        ao.setOption("swfPath", LangManager().getEntry("config.gfx.path.world.swf"))
        ao.setOption("tacticalModeTemplatesPath", LangManager().getEntry("config.atouin.path.tacticalModeTemplates"))
        Atouin().setDisplayOptions(ao)
        # StageShareManager.rootContainer.addEventListener(
        #     ScriptedAnimationEvent.SCRIPTED_ANIMATION_ADDED, onScriptedAnimationAdded
        # )
        dofusO = DofusOptions()
        DofusUI().setDisplayOptions(dofusO)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = DofusUI()
    print(StageShareManager().stageVisibleBounds)
    sys.exit(app.exec_())
