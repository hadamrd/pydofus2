from pydofus2.com.ankamagames.berilia.interfaces.IApi import IApi
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import PatternDecoder


class UiApi(IApi):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def isUiLoading(pUiName):
        return Berilia().loadingUi[pUiName]

    @staticmethod
    def replaceParams(text, params, replace="%"):
        return I18n.replaceParams(text, params, replace)

    @staticmethod
    def replaceKey(text):
        return LangManager().replaceKey(text, True)

    @staticmethod
    def getText(key, *params):
        return I18n.getUiText(key, params)

    @staticmethod
    def getTextFromKey(key, replace="%", *params):
        return I18n.getText(key, params, replace)

    @staticmethod
    def processText(str, gender, singular=True, zero=False):
        return PatternDecoder.combine(str, gender, singular, zero)

    @staticmethod
    def decodeText(str, params):
        return PatternDecoder.decode(str, params)
