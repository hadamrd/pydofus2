from PyQt5.QtCore import QObject, QRect, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from Stage import Stage


class StageShareManager(QObject):
    _instance = None
    _initialized = False
    _startWidth = 1280
    _startHeight = 1024
    _customMouseX = -77777
    _customMouseY = -77777
    windowScaleChanged = pyqtSignal(float)

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StageShareManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._rootContainer: QMainWindow = None
        self._isActive = False
        self._initialized = True
        self._stage = None
        self._stageVisibleBoundCache = QRect()
        self.stageLogicalBounds = None
        self.setupConnections()

    @property
    def rootContainer(self):
        return self._rootContainer

    @property
    def startWidth(self):
        return self._startWidth

    @property
    def startHeight(self):
        return self._startHeight

    def setupConnections(self):
        QApplication.instance().aboutToQuit.connect(self.onApplicationQuit)

    def onApplicationQuit(self):
        pass

    @property
    def stage(self) -> Stage:
        return self._stage

    @stage.setter
    def stage(self, value: Stage):
        self._stage = value
        self._startWidth = 1280
        self._startHeight = 1024
        if not self.stageLogicalBounds:
            self.stageLogicalBounds = QRect(0, 0, self._startWidth, self._startHeight)
        self.stage.setSceneRect(*self.stageLogicalBounds.getRect())

    @property
    def qMainWindow(self) -> QMainWindow:
        return self._rootContainer

    @qMainWindow.setter
    def qMainWindow(self, value: QMainWindow):
        self._rootContainer = value

    @property
    def mainWindow(self):
        return Stage().nativeWindow

    @property
    def chromeWidth(self):
        if self.mainWindow:
            return self.mainWindow.frameSize().width() - self.mainWindow.width()
        return None

    @property
    def chromeHeight(self):
        if self.mainWindow:
            return self.mainWindow.frameSize().height() - self.mainWindow.height()
        return None

    @property
    def windowScale(self):
        if self.mainWindow:
            stageWidth = self.mainWindow.width() / self._startWidth
            stageHeight = self.mainWindow.height() / self._startHeight
            return min(stageWidth, stageHeight)
        return 1

    @property
    def stageVisibleBounds(self):
        if self.mainWindow:
            windowWidth = self.mainWindow.width()
            windowHeight = self.mainWindow.height()
            stageWidthScale = windowWidth / self._startWidth
            stageHeightScale = windowHeight / self._startHeight
            if stageWidthScale > stageHeightScale:
                self._stageVisibleBoundCache.setWidth(max(windowWidth / stageHeightScale, self._startWidth))
                self._stageVisibleBoundCache.setHeight(self._startHeight)
                self._stageVisibleBoundCache.setX((self._startWidth - self._stageVisibleBoundCache.width()) / 2)
            else:
                self._stageVisibleBoundCache.setWidth(self._startWidth)
                self._stageVisibleBoundCache.setHeight(max(windowHeight * stageWidthScale, self._startHeight))
                self._stageVisibleBoundCache.setX(0)
                self._stageVisibleBoundCache.setY((self._startHeight - self._stageVisibleBoundCache.height()) / 2)
            if self._stageVisibleBoundCache.width() > self.stageLogicalBounds.width():
                self._stageVisibleBoundCache.setWidth(self.stageLogicalBounds.width())
            rightMargin = -(self.stageLogicalBounds.width() - self._startWidth) / 2
            if self._stageVisibleBoundCache.x() < rightMargin:
                self._stageVisibleBoundCache.setX(rightMargin)
            return self._stageVisibleBoundCache
        return QRect()
