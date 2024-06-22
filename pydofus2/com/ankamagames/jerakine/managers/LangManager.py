import re
import xml.etree.ElementTree as ET
from typing import Any

from click import FileError
from PyQt5.QtCore import QObject, pyqtSignal

from pydofus2.com.ankamagames.jerakine import JerakineConstants
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderFactory import ResourceLoaderFactory
from pydofus2.com.ankamagames.jerakine.resources.loaders.ResourceLoaderType import ResourceLoaderType
from pydofus2.com.ankamagames.jerakine.types.LangMetaData import LangMetaData
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.com.ankamagames.jerakine.utils.files.FileUtils import FileUtils


class LangManagerSignals(QObject):
    langAllFilesLoaded = pyqtSignal(str, bool)


class LangManager(metaclass=ThreadSharedSingleton):
    signals = LangManagerSignals()
    KEY_LANG_INDEX = "langIndex"
    KEY_LANG_CATEGORY = "langCategory"
    KEY_LANG_VERSION = "langVersion"

    def __init__(self) -> None:
        self._parseReference = dict()
        self._aLang: dict[str, Any] = StoreDataManager().getSetData(
            JerakineConstants.DATASTORE_LANG, self.KEY_LANG_INDEX, {}
        )
        self._aCategory: list = StoreDataManager().getSetData(
            JerakineConstants.DATASTORE_LANG, self.KEY_LANG_CATEGORY, list()
        )
        self._aVersion = StoreDataManager().getData(JerakineConstants.DATASTORE_LANG_VERSIONS, self.KEY_LANG_VERSION)
        Logger().debug(f"Lang version {self._aVersion}, Categories {self._aCategory}")
        self._loader = ResourceLoaderFactory.getLoader(ResourceLoaderType.SERIAL_LOADER)
        self._loader.resourceLoaded.connect(self.onFileLoaded)
        self._loader.loadFailed.connect(self.onFileError)

    def onFileLoaded(self, uri: Uri, resourceType, resource):
        if uri.fileType.upper() == "XML":
            self.onXmlLoadComplete(uri, resource)
        elif uri.fileType.upper() == "META":
            self.onMetaLoad(uri, resource)
        elif uri.fileType.upper() == "ZIP":
            self.onZipFileComplete(uri)

    def clear(self, sCategory=None):
        if sCategory:
            sCat = sCategory + "."
            keys_to_delete = [s for s in self._aLang if s.startswith(sCat)]
            for s in keys_to_delete:
                del self._aLang[s]
        else:
            self._aLang = {}
        StoreDataManager().setData(JerakineConstants.DATASTORE_LANG, self.KEY_LANG_INDEX, self._aLang)

    def onXmlLoadComplete(self, uri: Uri, resource):
        metaData: LangMetaData = uri.tag
        sCat = FileUtils.getFileStartName(uri.uri)
        if sCat == "config-custom" or "config-lang-" in sCat:
            sCat = "config"
        if uri.fileName in metaData.clearFile or metaData.clearAllFile or metaData.loadAllFile:
            if uri.fileName in metaData.clearFile or metaData.clearAllFile:
                self.clear(sCat)
            self.startParsing(resource, sCat, uri.uri, metaData)
            self.signals.langAllFilesLoaded.emit(uri.path, True)

    def startParsing(self, content, category, sUrlProvider, metaData: LangMetaData = None):
        StoreDataManager().startStoreSequence()
        parseReference = self._parseReference[sUrlProvider]
        self.parseXml(content, category, parseReference)
        if metaData and metaData.clearFile.get(sUrlProvider):
            self.setFileVersion(
                FileUtils.getFileStartName(sUrlProvider) + "." + sUrlProvider, metaData.clearFile[sUrlProvider]
            )

    def setFileVersion(self, sFileName: str, sVersion: str):
        self._aVersion[sFileName] = sVersion
        StoreDataManager().setData(JerakineConstants.DATASTORE_LANG_VERSIONS, self.KEY_LANG_VERSION, self._aVersion)

    def parseXml(self, sXml, sCategory, parseReferences):
        self._aCategory.append(sCategory)
        StoreDataManager().getSetData(JerakineConstants.DATASTORE_LANG, "langCategory", self._aCategory)
        try:
            xml = ET.fromstring(sXml)
            for entry in xml.findall(".//entry"):
                if parseReferences:
                    sEntry = self.replaceKey(entry.text)
                else:
                    sEntry = entry.text
                entryType = entry.get("type") if entry.get("type") else None
                self.setEntry(sCategory + "." + entry.get("key"), sEntry, entryType)
        except ET.ParseError as e:
            Logger().error("Parsing error on category " + str(sCategory) + ": " + str(e))
        except Exception as e:
            Logger().error("An unexpected error occurred: " + str(e))

    def onMetaLoad(self, uri: Uri, resource):
        self.loadLangFile(uri.tag, LangMetaData.fromXml(resource, uri.tag, self.checkFileVersion))

    def checkFileVersion(self, sFileName, sVersion):
        return self._aVersion[sFileName] == sVersion

    def loadLangFile(self, sUrl: str, oMeta: LangMetaData):
        sExtension = FileUtils.getExtension(sUrl)
        if sExtension is None:
            raise FileError(sUrl, "Unable to determine file extension")
        if not oMeta.clearAllFile and not oMeta.clearFileCount and not oMeta.loadAllFile:
            self.signals.langAllFilesLoaded.emit(sUrl, True)
            return
        uri = Uri(sUrl)
        uri.tag = oMeta
        if sExtension.upper() == "ZIP":
            Logger().warning("Loading zip")
        elif sExtension.upper() == "XML":
            pass
        else:
            raise FileError(
                sUrl, "Unexpected type (bad extension found (" + sExtension + "), support only .zip and .xml)."
            )
        self._loader.load(uri)

    def onZipFileComplete(self):
        ...

    def onFileError(self, uri: Uri, errorMessage, errorCode):
        ...

    def replaceKey(self, sTxt: str, bReplaceDynamicReference=False):
        from pydofus2.com.ankamagames.jerakine.data.I18n import I18n

        if sTxt is not None and "[" in sTxt:
            reg = re.compile(r"(?<!\\)\[([^\]]*)\]")
            aKey = reg.findall(sTxt)
            if "\\[" in sTxt:
                sTxt = sTxt.replace("\\[", "[")
            for sKey in aKey:
                if sKey[0] == "#":
                    if not bReplaceDynamicReference:
                        continue
                    sKey = sKey[1:]
                sNewVal = str(self._aLang.get(sKey, None))
                if sNewVal is None:
                    if int(sKey) > 0:
                        sNewVal = I18n.getText(int(sKey))
                    if I18n.hasUiText(sKey):
                        sNewVal = I18n.getUiText(sKey)
                    if sKey[0] == "~":
                        continue
                    if sNewVal is None:
                        sNewVal = f"[{sKey}]"
                        aFind = self.getCategory(sKey)
                        if len(aFind) > 0:
                            Logger().error(
                                f"Incorrect reference to the key [{sKey}] in : {sTxt} (could be {' or '.join(aFind)})"
                            )
                        else:
                            Logger().error(f"Unknown reference to the key [{sKey}] in : {sTxt}")
                sTxt = sTxt.replace(f"[{sKey}]", sNewVal)
        return sTxt

    def getUntypedEntry(self, sKey):
        langData = StoreDataManager().getData(JerakineConstants.DATASTORE_LANG, self.KEY_LANG_INDEX)
        sEntry = langData.get(sKey, None)
        if sEntry is None:
            Logger().warning(f"[Warning] LangManager : {sKey} is unknown")
            sEntry = "!" + sKey
        if sEntry is not None and isinstance(sEntry, str) and "[" in sEntry:
            sEntry = self.replaceKey(sEntry, True)
        return sEntry

    def getEntry(self, key):
        return self.getUntypedEntry(key)

    def getIntEntry(self, key: str) -> int:
        return int(self.getUntypedEntry(key))

    def getCategory(self, sCategory, matchSubCategories=True):
        aResult = {}
        for key in self._aLang.keys():
            if matchSubCategories:
                if key == sCategory or key.startswith(sCategory):
                    aResult[key] = self._aLang[key]
        return aResult

    def setEntry(self, sKey: str, sValue: str, sType: str = ""):
        if not sType:
            self._aLang[sKey] = sValue
        else:
            sType = sType.upper()
            if sType == "STRING":
                self._aLang[sKey] = sValue
            elif sType == "NUMBER":
                self._aLang[sKey] = float(sValue)
            elif sType in ["UINT", "INT"]:
                self._aLang[sKey] = int(sValue, 10)
            elif sType == "BOOLEAN":
                self._aLang[sKey] = sValue.lower() == "true"
            elif sType == "ARRAY":
                self._aLang[sKey] = sValue.split(",")
            else:
                self._aLang[sKey] = globals()[sType](sValue)

    def findCategory(self, s_key: str) -> list:
        s_k = s_key.split(".")[0]
        a_cat = []

        for s in self._aCategory:
            if f"{s}.{s_k}" in self._aLang:
                a_cat.append(f"{s}.{s_k}")

        for s in self._aCategory:
            if f"{s}.{s_key}" in self._aLang:
                a_cat.append(f"{s}.{s_key}")

        return a_cat

    def loadFile(self, sUrl: str, parseReference: bool = True):
        if parseReference:
            self._parseReference[Uri(sUrl).uri] = parseReference
        self.loadMetaDataFile(sUrl)

    def loadMetaDataFile(self, sUrl: str):
        sMetaDataUrl = FileUtils.getFilePathStartName(sUrl) + ".meta"
        uri = Uri(sMetaDataUrl)
        uri.tag = sUrl
        self._loader.load(uri)


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    Logger.logToConsole = True
    app = QApplication(sys.argv)
    LangManager().loadFile("config.xml")
    LangManager().signals.langAllFilesLoaded.connect(lambda uri, bSuccess: app.quit())
    sys.exit(app.exec_())
