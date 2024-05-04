import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGraphicsView, QMainWindow
from Stage import Stage
from StageShareManager import StageShareManager

from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.atouin.types.AtouinOptions import AtouinOptions
from pydofus2.com.ankamagames.atouin.types.DataMapContainer import DataMapContainer
from pydofus2.com.ankamagames.atouin.types.SimpleGraphicsContainer import SimpleGraphicsContainer
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.types.DofusOptions import DofusOptions
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.types.CustomSharedObject import CustomSharedObject
from pydofus2.com.ankamagames.jerakine.types.events.PropertyChangeEvent import PropertyChangeEvent
from pydofus2.DofusUI.OptionManager import OptionManager


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
        self._windowInitialized = False
        self._worldContainer = SimpleGraphicsContainer()
        self.stage.addItem(self._worldContainer)
        StageShareManager().stage = self.stage
        StageShareManager().qMainWindow = self
        self.initOptions()

    def initWindow(self, isFullScreen):
        if self._windowInitialized:
            return

        self._windowInitialized = True

        clientDimensionSo = CustomSharedObject.getLocal("clientData")

        mainScreen = QScreen.availableGeometry(QApplication.primaryScreen())

        if clientDimensionSo.data.get("width") > 0 and clientDimensionSo.data.get("height") > 0:
            self.resize(clientDimensionSo.data["width"], clientDimensionSo.data["height"])
            if not isFullScreen and clientDimensionSo.data.get("displayState") == "maximized":
                self.setWindowState(Qt.WindowMaximized)

        else:
            self.resize(mainScreen.width() * 0.8, mainScreen.height() * 0.8)
            self.setWindowState(Qt.WindowMaximized)

        self.centerOnScreen()
        self.show()

    def centerOnScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setDisplayOptions(self, opt: DofusOptions):
        self.initWindow(opt.getOption("fullScreen"))
        self._doOptions = opt
        self._doOptions.on(PropertyChangeEvent.PROPERTY_CHANGED, self.onOptionChange)
        self._doOptions.setOption("flashQuality", self._doOptions.getOption("flashQuality"))
        self._doOptions.setOption("fullScreen", self._doOptions.getOption("fullScreen"))

    def onOptionChange(self, e, name, value, oldValue):
        Logger().info(f"DofusUI property {name} changed from {oldValue} to {value}")

    def getWorldContainer(self):
        return self._worldContainer

    def initOptions(self):
        from pydofus2.com.ankamagames.atouin.Atouin import Atouin
        from pydofus2.com.ankamagames.atouin.Frustum import Frustum

        OptionManager.reset()
        ao = AtouinOptions(self.getWorldContainer(), Kernel().worker)
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
        ao.setOption("swfPath", XmlConfig().getEntry("config.gfx.path.world.swf"))
        ao.setOption("tacticalModeTemplatesPath", LangManager().getEntry("config.atouin.path.tacticalModeTemplates"))
        Atouin().setDisplayOptions(ao)
        self.setDisplayOptions(DofusOptions())

    def saveClientSize(self):
        clientDimensionSo = CustomSharedObject.getLocal("clientData")
        clientDimensionSo.data["height"] = self.width()
        clientDimensionSo.data["width"] = self.height()
        clientDimensionSo.data["displayState"] = (
            "maximized" if self.windowState() == Qt.WindowMaximized else str(self.windowState())
        )
        clientDimensionSo.flush()
        clientDimensionSo.close()

    def beforeExit(self):
        # This is the method you want to execute before the window closes
        print("Executing beforeExit: performing cleanup or saving settings.")
        self.saveClientSize()

    def closeEvent(self, event):
        # This method is automatically called when the window is about to close
        self.beforeExit()  # Call your method here
        event.accept()  # Proceed with the window closure


if __name__ == "__main__":
    import sys

    Logger.logToConsole = True
    app = QApplication(sys.argv)
    main_window = DofusUI()
    from pydofus2.com.ankamagames.atouin.Atouin import Atouin
    from pydofus2.DofusUI.MapRenderer import MapRenderer

    mapRenderer = MapRenderer(Atouin().worldContainer, Elements())
    mapId = 191104002.0
    MapDisplayManager().loadMap(mapId)
    dataMap = DataMapContainer(MapDisplayManager().dataMap)
    mapRenderer.render(dataMap)
    sys.exit(app.exec_())
