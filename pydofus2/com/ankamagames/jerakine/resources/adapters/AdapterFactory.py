from pydofus2.com.ankamagames.jerakine.resources.adapters.IAdapter import IAdapter
from pydofus2.com.ankamagames.jerakine.resources.adapters.impl.BitMapAdapter import BitmapAdapter
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri
from pydofus2.com.ankamagames.jerakine.utils.files.FileUtils import FileUtils


class ResourceError(Exception):
    pass


class AdapterFactory:

    _customAdapters = dict()

    @staticmethod
    def getAdapter(uri: Uri) -> IAdapter:
        uriFileType = uri.fileType
        if uriFileType.lower() in ["xml", "meta", "dm", "dt"]:
            return XmlAdapter()
        elif uriFileType.lower() in ["png", "gif", "jpg", "jpeg"]:
            return BitmapAdapter()
        elif uriFileType.lower() in ["txt", "css"]:
            return TxtAdapter()
        elif uriFileType.lower() == "swf":
            return SwfAdapter()
        elif uriFileType.lower() == "aswf":
            return AdvancedSwfAdapter()
        elif uriFileType.lower() == "swl":
            return SwlAdapter()
        elif uriFileType.lower() == "zip":
            return ZipAdapter()
        elif uriFileType.lower() == "mp3":
            return MP3Adapter()
        elif uriFileType.lower() == "json":
            return JSONAdapter()
        else:
            if uri.subPath and FileUtils.getExtension(uri.path) == "swf":
                return AdvancedSwfAdapter()
            customAdapter = AdapterFactory._customAdapters.get(uriFileType)
            if customAdapter:
                ca = customAdapter()
                if not isinstance(ca, IAdapter):
                    raise ResourceError(
                        f"Registered custom adapter for extension {uriFileType} isn't an IAdapter class."
                    )
                return ca

            if uriFileType.endswith("s"):
                return SignedFileAdapter()

            return BinaryAdapter()

    @staticmethod
    def addAdapter(extension: str, adapter: type) -> None:
        AdapterFactory._customAdapters[extension] = adapter

    @staticmethod
    def removeAdapter(extension: str) -> None:
        AdapterFactory._customAdapters.pop(extension, None)
