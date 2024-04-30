from PyQt5.QtWidgets import QGraphicsScene, QMainWindow


class Stage(QGraphicsScene):
    _instance = None
    _initialized = False

    def __new__(cls, nativeWindow=None):
        if cls._instance is None:
            cls._instance = super(Stage, cls).__new__(cls)
            cls._instance.__init__(nativeWindow)
        return cls._instance

    def __init__(self, nativeWindow: QMainWindow = None):
        if self._initialized:
            return
        self.nativeWindow = nativeWindow
        Stage._initialized = True
        super().__init__()
