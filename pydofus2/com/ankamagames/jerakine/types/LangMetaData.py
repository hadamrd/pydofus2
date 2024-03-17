from xml.etree.ElementTree import Element, ElementTree

from pydofus2.com.ankamagames.jerakine.utils.files.FileUtils import FileUtils


class LangMetaData:
    def __init__(self):
        self._nFileCount = 0
        self.loadAllFile = False
        self.clearAllFile = False
        self.clearOnlyNotUpToDate = True
        self.clearFile = {}

    @staticmethod
    def fromXml(sXml, sUrlProvider, checkFunction):
        tree = ElementTree(Element(sXml))
        metaData = LangMetaData()
        bHaveVersionData = False

        filesActions = tree.findall("filesActions")

        for fileActions in filesActions:
            clearOnlyNotUpToDate = fileActions.findtext("clearOnlyNotUpToDate")
            if clearOnlyNotUpToDate == "true":
                metaData.clearOnlyNotUpToDate = True
            elif clearOnlyNotUpToDate == "false":
                metaData.clearOnlyNotUpToDate = False

            loadAllFile = fileActions.findtext("loadAllFile")
            if loadAllFile == "true":
                metaData.loadAllFile = True
            elif loadAllFile == "false":
                metaData.loadAllFile = False

            clearAllFile = fileActions.findtext("clearAllFile")
            if clearAllFile == "true":
                metaData.clearAllFile = True
            elif clearAllFile == "false":
                metaData.clearAllFile = False

        for file in tree.findall("filesVersions/file"):
            bHaveVersionData = True
            fileName = file.attrib['name']
            fileString = file.text
            if metaData.clearAllFile or not metaData.clearOnlyNotUpToDate or not checkFunction(FileUtils.getFileStartName(sUrlProvider) + "." + fileName, fileString):
                metaData.addFile(fileName, fileString)

        if not bHaveVersionData:
            metaData.loadAllFile = True

        return metaData

    def addFile(self, sFilename, sVersion):
        self._nFileCount += 1
        self.clearFile[sFilename] = sVersion

    @property
    def clearFileCount(self):
        return self._nFileCount
