from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event, EventsHandler
from pydofus2.com.ankamagames.jerakine import JerakineConstants
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType

# from pydofus2.com.ankamagames.jerakine.types.events.FileEvent import FileEvent
from pydofus2.com.ankamagames.jerakine.types.LangMetaData import LangMetaData
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.com.ankamagames.jerakine.utils.files.FileUtils import FileUtils


class DataUpdateManager(EventsHandler):
    SQL_MODE = XmlConfig().getEntry("config.data.SQLMode") == "true"

    def __init__(self):
        super().__init__()
        self._log = Logger()
        self._loader = None
        self._versions = None
        self._dataFilesLoaded = False
        self._files = None
        self._loadedFileCount = 0
        self._metaFileListe = None
        self._storeKey = None
        self._clearAll = None
        self._datastoreList = None

    def init(self, metaFileListe: Uri, clearAll=False):
        self._metaFileListe = metaFileListe
        self._storeKey = "version_" + self._metaFileListe.uri
        self._clearAll = clearAll
        if self._clearAll:
            self.clear()
        self.initMetaFileListe()

    def initMetaFileListe(self):
        self._versions = (
            []
            if self._clearAll
            else StoreDataManager().getSetData(JerakineConstants.DATASTORE_FILES_INFO, self._storeKey, [])
        )
        self._files = []
        self._loader = ResourceLoaderFactory.getLoader(ResourceLoaderType.SERIAL_LOADER)
        self._loader.on(ResourceEvent.LOADER_COMPLETE, self.onComplete)
        self._loader.on(ResourceEvent.LOADED, self.onLoaded)
        self._loader.on(ResourceEvent.ERROR, self.onLoadFailed)
        self._loader.load(self._metaFileListe)

    @property
    def files(self):
        return self._files

    def clear(self):
        pass

    def checkFileVersion(self, sFileName, sVersion):
        return self._versions[sFileName] == sVersion

    def onLoaded(self, uri: Uri, resource):
        if uri.fileType == "meta":
            meta = LangMetaData.fromXml(resource, uri.uri, self.checkFileVersion)
            for file in meta.clearFile:
                uri = Uri(FileUtils.getFilePath(uri.path) + "/" + file)
                uri.tag = {"version": meta.clearFile[file], "file": FileUtils.getFileStartName(uri.uri) + "." + file}
                self._files.append(uri)
            if meta.clearFileCount:
                self._loader.load(self._files)
            else:
                self.send(Event.COMPLETE)
        elif uri.fileType == "swf":
            self._dataFilesLoaded = True
            container = resource
            StoreDataManager().setData(
                JerakineConstants.DATASTORE_FILES_INFO, container.moduleName + "_filelist", container.fileList
            )
            StoreDataManager().setData(
                JerakineConstants.DATASTORE_FILES_INFO, container.moduleName + "_chunkLength", container.chunkLength
            )
            self._loadedFileCount += 1

    def onLoadFailed(self, uri: Uri):
        self._log.error("Failed " + uri)
        self.send(FileEvent.ERROR, uri.uri, False)

    def onComplete(self, e):
        self._loader.removeListener(ResourceEvent.LOADER_COMPLETE, self.onComplete)
        self._loader.removeListener(ResourceEvent.LOADED, self.onLoaded)
        self._loader.removeListener(ResourceEvent.ERROR, self.onLoadFailed)
        if self._dataFilesLoaded:
            self.send(Event.COMPLETE)
