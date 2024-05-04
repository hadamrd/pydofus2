from PyQt5.QtGui import QImage


class ColorTransform:
    def __init__(self, redMultiplier, greenMultiplier, blueMultiplier, alpha):
        self.redMultiplier = redMultiplier
        self.greenMultiplier = greenMultiplier
        self.blueMultiplier = blueMultiplier
        self.alphaMultiplier = alpha

    def apply(self, image: QImage) -> QImage:
        if image.format() != QImage.Format_ARGB32:
            image = image.convertToFormat(QImage.Format_ARGB32)

        redm = self.redMultiplier / 127 + 1
        greenm = self.greenMultiplier / 127 + 1
        bluem = self.blueMultiplier / 127 + 1
        alpham = self.alphaMultiplier / 255
        width, height = image.width(), image.height()

        buffer = image.bits()  # This is a sip.voidptr
        buffer.setsize(image.byteCount())  # Required to access data correctly

        # Access image buffer as a bytearray for easy manipulation
        arr = bytearray(buffer)

        # Efficient access to pixel data using index calculation
        for y in range(height):
            for x in range(width):
                i = (y * width + x) * 4  # Calculate index for the pixel
                r, g, b, a = arr[i : i + 4]  # Extract RGBA values

                # Apply transformations
                r = min(255, int(round(r * redm)))
                g = min(255, int(round(g * greenm)))
                b = min(255, int(round(b * bluem)))
                a = min(255, int(round(a * alpham)))

                # Update the array with new values
                arr[i : i + 4] = bytes([r, g, b, a])

        # Convert bytearray back to voidptr to update the image
        buffer[:] = arr
        return image
