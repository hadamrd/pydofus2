from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event
from pydofus2.com.ankamagames.jerakine import JerakineConstants
from pydofus2.com.ankamagames.jerakine.data.DataUpdateManager import \
    DataUpdateManager
from pydofus2.com.ankamagames.jerakine.data.I18nFileAccessor import \
    I18nFileAccessor
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import \
    StoreDataManager
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.events.LangFileEvent import \
    LangFileEvent
from pydofus2.com.ankamagames.jerakine.types.LangMetaData import LangMetaData
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.com.ankamagames.jerakine.utils.files.FileUtils import FileUtils


class I18nUpdater(DataUpdateManager, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self._language = None
        self._overrideProvider = None

    def initI18n(self, language: str, metaFileListe: Uri, clearAll=False, overrideProvider=None):
        self._language = language
        self._overrideProvider = overrideProvider
        super().init(metaFileListe, clearAll)

    def checkFileVersion(self, sFileName, sVersion):
        return False

    def clear(self):
        I18nFileAccessor().close()

    def onLoaded(self, event_id, uri: Uri, resource):
        if uri.fileType == "d2i":
            I18nFileAccessor().initI18n(uri)
            if self._overrideProvider:
                I18nFileAccessor().addOverrideFile(self._overrideProvider)
            self._versions[uri.tag["file"]] = uri.tag["file"]
            StoreDataManager().setData(JerakineConstants.DATASTORE_FILES_INFO, self._storeKey, self._versions)
            self.send(LangFileEvent.COMPLETE, uri.tag["file"])
            self._dataFilesLoaded = True
            self._loadedFileCount += 1
        elif uri.fileType == "meta":
            meta = LangMetaData.fromXml(resource, uri.uri, self.checkFileVersion)
            realCount = 0
            for file in meta.clearFile:
                if "_" + self._language in file:
                    uri = Uri(FileUtils.getFilePath(uri.path) + "/" + file)
                    uri.tag = {
                        "version": meta.clearFile[file],
                        "file": FileUtils.getFileStartName(uri.uri) + "." + file,
                    }
                    self._files.append(uri)
                    realCount += 1
            if realCount:
                self._loader.load(self._files)
            else:
                self.send(Event.COMPLETE)
        else:
            super().onLoaded(event_id, uri, resource)
