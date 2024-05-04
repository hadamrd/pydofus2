from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QGraphicsPixmapItem


class AnimatedGifItem(QGraphicsPixmapItem):
    def __init__(self, gif_path=None, parent=None):
        super(AnimatedGifItem, self).__init__(parent)
        self.movie = QMovie(gif_path) if gif_path else QMovie()
        self.movie.frameChanged.connect(self.updatePixmap)

    def setGifPath(self, path):
        self.movie.setFileName(path)
        self.movie.start()  # Start the movie as soon as the path is set

    def updatePixmap(self, frame_number):
        self.setPixmap(self.movie.currentPixmap())

    def play(self):
        if self.movie.state() in [QMovie.NotRunning, QMovie.Paused]:
            self.movie.start()

    def pause(self):
        if self.movie.state() == QMovie.Running:
            self.movie.setPaused(True)

    def resume(self):
        self.movie.setPaused(False)

    def stop(self):
        self.movie.stop()

    def boundingRect(self):
        return QRectF(self.pixmap().rect())
