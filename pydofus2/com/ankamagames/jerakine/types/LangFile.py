from pydofus2.com.ankamagames.jerakine.types.LangMetaData import LangMetaData


class LangFile:
    def __init__(self, sContent: str, sCategory: str, sUrl: str, oMeta: LangMetaData = None):
        self.content = sContent
        self.url = sUrl
        self.category = sCategory
        self.metaData = oMeta
