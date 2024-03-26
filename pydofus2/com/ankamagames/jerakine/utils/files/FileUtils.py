from typing import Optional


class FileUtils:

    @staticmethod
    def getExtension(sUrl: str) -> Optional[str]:
        if not sUrl or sUrl.rfind(".") == -1:
            return None
        return sUrl[sUrl.rfind(".") + 1 :]

    @staticmethod
    def getFileName(sUrl: str) -> str:
        return sUrl[sUrl.rfind("/") + 1 :]

    @staticmethod
    def getFilePath(sUrl: str) -> str:
        if sUrl.find("/") != -1:
            return sUrl[0 : sUrl.rfind("/")]
        if sUrl.find("\\") != -1:
            return sUrl[0 : sUrl.rfind("\\")]
        return ""

    @staticmethod
    def getFilePathStartName(sUrl: str) -> str:
        return sUrl[0 : sUrl.rfind(".")]

    @staticmethod
    def getFileStartName(sUrl: str) -> str:
        return sUrl[sUrl.rfind("/") + 1 : sUrl.rfind(".")]
