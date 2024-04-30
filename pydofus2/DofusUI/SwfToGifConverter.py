import io
import subprocess
import tempfile

from PyQt5.QtGui import QMovie

from pydofus2.com.ankamagames.atouin.Atouin import Atouin
from pydofus2.com.ankamagames.dofus import settings
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class SwfConverter:
    GIF_FOLDER = settings.PYDOFUS2_APPDIR / "gif"

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self._swfGfx = {}
        self._gfxPath = Atouin().options.getOption("elementsPath")
        self._gfxPathSwf = Atouin().options.getOption("swfPath")
        self.initSwfLoader()

    def initSwfLoader(self):
        self._swfLoader = ResourceLoaderFactory.getLoader(ResourceLoaderType.PARALLEL_LOADER)
        self._swfLoader.on(ResourceEvent.ERROR, self.onLoadError)
        self._swfLoader.on(ResourceEvent.LOADED, self.onSwfLoaded)
        self._swfLoader.on(ResourceEvent.LOADER_COMPLETE, self.onAllSwfLoaded)
        self._swfLoader.on(ResourceEvent.LOADER_PROGRESS, self.onLoadingProgress)

    def loadSwfList(self, uris: list[Uri]):
        self._swfLoader.load(uris)

    def onloadError(self, event, uri, errorMsg, errorCode):
        Logger().error(f"Load of resource at uri: {uri} failed with err[{errorCode}] {errorMsg}")

    def onSwfLoaded(self, event, uri, resourceType, swf_stream: io.BytesIO):
        output_path = self.convertSwfToGif(swf_stream, uri.tag)
        movie = QMovie(output_path)
        self._swfGfx[uri.tag] = movie

    def onAllSwfLoaded(self, event):
        print("All SWF files have been processed.")
        self.callback(self._swfGfx)

    def onLoadingProgress(self, event):
        pass

    def convertSwfToGif(self, swf_stream, gfx_id):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".swf") as tmp:
            tmp.write(swf_stream.read())
            tmp.flush()
            output_path = self.GIF_FOLDER / f"{gfx_id}.gif"
            subprocess.run(["ffmpeg", "-i", tmp.name, output_path], stdout=subprocess.PIPE)
            return output_path
