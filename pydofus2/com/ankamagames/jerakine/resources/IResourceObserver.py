class IResourceObserver:
    def onLoaded(self, uri, param2, param3):
        ...

    def onFailed(self, uri, param2, param3):
        ...

    def onProgress(self, uri, param2, param3):
        ...
