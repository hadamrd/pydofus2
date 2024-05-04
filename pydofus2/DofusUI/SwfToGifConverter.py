import io
import os
import subprocess
import tempfile

from pydofus2.com.ankamagames.dofus import settings
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.DofusUI.AnimatedGifItem import AnimatedGifItem
from pydofus2.DofusUI.GfxParallelLoader import GfxParallelLoader


class SwfConverter:
    GIF_FOLDER = settings.PYDOFUS2_APPDIR / "gif"

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self._swfGfx = {}
        self.initSwfLoader()

    def initSwfLoader(self):
        self._swfLoader = GfxParallelLoader(maxThreads=6)
        self._swfLoader.progress.connect(self.onSwfLoaded)
        self._swfLoader.error.connect(self.onLoadError)
        self._swfLoader.finished.connect(self.onAllSwfLoaded)

    def loadSwfList(self, uris: list[Uri]):
        self._swfLoader.loadItems(uris)

    def onLoadError(self, gfxId, exc: Exception):
        Logger().error(f"Load of resource {gfxId} failed with {exc}")

    def onSwfLoaded(self, resourceId, resourceData: io.BytesIO):
        output_path = self.convertSwfToGif(resourceData, resourceId)
        self._swfGfx[resourceId] = AnimatedGifItem(output_path)

    def onAllSwfLoaded(self):
        print("All SWF files have been processed.")
        self.callback(self._swfGfx)

    def convertSwfToGif(self, resourceData: io.BytesIO, resourceId):
        if not os.path.exists(self.GIF_FOLDER):
            os.makedirs(self.GIF_FOLDER)
        output_path = self.GIF_FOLDER / f"{resourceId}.gif"
        if os.path.exists(output_path):
            return output_path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".swf") as tmp:
            tmp.write(resourceData.read())
            tmp.flush()
            subprocess.run(["ffmpeg", "-i", tmp.name, output_path], stdout=subprocess.PIPE)
            return output_path
