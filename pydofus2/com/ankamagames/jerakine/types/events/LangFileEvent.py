class LangFileEvent:
    ALL_COMPLETE = "LangFileEvent_ALL_COMPLETE"
    COMPLETE = "LangFileEvent_COMPLETE"

    def __init__(self, event_type, bubbles=False, cancelable=False, sUrl=None, sUrlProvider=None):
        self.type = event_type
        self.bubbles = bubbles
        self.cancelable = cancelable
        self._sUrl = sUrl
        self._sUrlProvider = sUrlProvider

    def clone(self):
        return LangFileEvent(self.type, self.bubbles, self.cancelable, self._sUrl, self._sUrlProvider)

    @property
    def url(self):
        return self._sUrl

    @property
    def urlProvider(self):
        return self._sUrlProvider
