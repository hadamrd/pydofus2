import numpy as np
from PyQt5.QtGui import QImage


def qimage_to_numpy(image):
    ptr = image.bits()
    ptr.setsize(image.byteCount())
    arr = np.array(ptr, dtype=np.uint8).reshape((image.height(), image.width(), 4))
    return arr


class ColorTransform:
    def __init__(self, redMultiplier, greenMultiplier, blueMultiplier, alpha):
        self.redMultiplier = redMultiplier
        self.greenMultiplier = greenMultiplier
        self.blueMultiplier = blueMultiplier
        self.alphaMultiplier = alpha

    def apply(self, image: QImage) -> QImage:
        if image.format() != QImage.Format_ARGB32:
            image = image.convertToFormat(QImage.Format_ARGB32)
        image_data = qimage_to_numpy(image)
        multipliers = np.array([self.redMultiplier, self.greenMultiplier, self.blueMultiplier, self.alphaMultiplier])
        image_data = image_data.astype(np.float32)
        image_data = np.clip(image_data * multipliers[np.newaxis, np.newaxis, :], 0, 255).astype(np.uint8)
        return QImage(image_data.data, image.width(), image.height(), image.bytesPerLine(), QImage.Format_ARGB32)
