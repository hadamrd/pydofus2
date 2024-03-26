class IStatsClass:

    def process(self, pMessage, pArgs=None):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()
