import hashlib
import platform
from pathlib import Path
from urllib.parse import urlparse

from pydofus2.com.ankamagames.dofus import Constants


class Uri:
    subPathDelimiter = "|"

    def __init__(self, uri=None, tag=None):
        self._protocol = None
        self._path: str = None
        self._subPath: str = None
        self._secureMode = False  # Assuming secure mode to be False initially
        self._useSecureURI = False  # Assuming use secure URI to be False initially
        self._uri = uri
        self._uriChanged = True
        self._fileNameChanged = True
        self._fileTypeChanged = True
        self.tag = tag
        self.parseUri(uri)

    def parseUri(self, uri: str):
        if not uri:
            return
        url = urlparse(uri)
        self._protocol = url.scheme if url.scheme else "file"
        path = Path(url.netloc + url.path)
        str_path = str(path)
        if self.subPathDelimiter in str_path:
            self.path, self.subPath = str_path.split(self.subPathDelimiter, 1)
        else:
            self.path = str_path
            self.subPath = None
        if (
            self._secureMode
            and self._useSecureURI
            and self._protocol == "file"
            and not self.isSecure()
        ):
            raise ValueError(f"'{uri}' is an insecure URI.")

    def isSecure(self):
        # This needs to be implemented according to your requirements
        return True

    def toString(self):
        return f"{self._protocol}://{self._path}" + (
            f"|{self._subPath}" if self._subPath else ""
        )
        
    def __str__(self) -> str:
        return self.toString()
    
    def __repr__(self) -> str:
        return self.toString()
    
    def toSum(self):
        return hashlib.md5(self.toString().encode()).hexdigest()

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value
        self._uri = self.toString()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        path_obj = Path(value)
        self._path = str(path_obj.resolve())
        if platform.system() == "Windows":
            if self._path.startswith("/"):
                for i in range(1, len(self._path)):
                    if self._path[i] != "/":
                        break
                self._path = "\\\\" + self._path[i:]
            if "//" in self._path:
                self._path = self._path.replace("//", "/")
        self._sum = ""
        self._uriChanged = True
        self._fileNameChanged = True
        self._fileTypeChanged = True

    @property
    def subPath(self):
        return self._subPath

    @subPath.setter
    def subPath(self, value):
        if (not self.subPath and not value) or (
            self.subPath
            and value
            and len(self.subPath) == len(value)
            and self.subPath.startswith(value)
        ):
            return
        if value is None or value == "":
            self._subPath = None
        else:
            value = Path(value).as_posix()
            self._subPath = value[1:] if value[0] == "/" else value
        self._sum = ""
        self._uriChanged = True
        self._fileNameChanged = True
        self._fileTypeChanged = True

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self.parseUri(value)

    def toFile(self) -> Path:
        if not self._path:
            tmp = Path("null")
        else:
            tmp = Path(self._path)
        if tmp.is_absolute():
            return tmp
        if self._protocol == "mod":
            from pydofus2.com.ankamagames.jerakine.managers.LangManager import \
                LangManager

            uiRoot = Path(LangManager().getEntry("config.mod.path"))
            if not uiRoot.is_absolute():
                return Constants.DOFUS_ROOTDIR / uiRoot / tmp
            return uiRoot / tmp
        return Constants.DOFUS_ROOTDIR / tmp

    @property
    def fileType(self):
        if self._fileTypeChanged:
            path_obj = (
                Path(self._subPath)
                if self._subPath and "." in self._subPath
                else Path(self._path)
            )
            file_suffix = path_obj.suffix.split("?")[0]
            self._fileType = file_suffix[1:] if file_suffix.startswith(".") else file_suffix
            self._fileTypeChanged = False
        return self._fileType

    def normalizedUri(self) -> str:
        supported_protocols = ["http", "https", "file", "zip", "mod", "theme", "d2p", "d2pOld", "pak", "pak2"]
        if self._protocol in supported_protocols:
            return self._uri.replace("/\\/g", "/")
        else:
            raise ValueError(f"Unsupported protocol {self._protocol} for normalization.")
    
    def normalizedUriWithoutSubPath(self) -> str:
        supported_protocols = ["http", "https", "file", "zip", "mod", "theme", "d2p", "d2pOld", "pak", "pak2"]
        if self._protocol in supported_protocols:
            return self.toString().replace("/\\/g", "/")
        else:
            raise ValueError(f"Unsupported protocol {self._protocol} for normalization.")