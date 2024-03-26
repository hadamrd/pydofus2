class ResourceEvent:
    LOADED = "loaded"
    LOADER_PROGRESS = "load_progress"
    ERROR = "error"
    LOADER_COMPLETE = "load_complete"
    PROGRESS = "progress"

    def __init__(self, type_: str, bubbles: bool = False, cancelable: bool = False):
        self.type_ = type_
        self.bubbles = bubbles
        self.cancelable = cancelable

    def clone(self):
        return ResourceEvent(self.type_, self.bubbles, self.cancelable)
