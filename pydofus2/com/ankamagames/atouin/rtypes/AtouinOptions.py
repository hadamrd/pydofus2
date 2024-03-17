from pydofus2.com.ankamagames.jerakine.managers.OptionManager import \
    OptionManager


class AtouinOptions(OptionManager):

    def __init__(self, docContainer, mhHandler):
        super().__init__("atouin")
        self._container = docContainer
        self._handler = mhHandler

        # Assuming 'add' method adds options with default values
        self.add("groundCacheMode", 1)
        self.add("useInsideAutoZoom", False)
        self.add("useCacheAsBitmap", False)
        self.add("useSmooth", True)
        # self.add("frustum", Frustum())
        self.add("alwaysShowGrid", False)
        self.add("showCellIdOnOver", False)
        self.add("showEveryCellId", False)
        # self.add(EnterFrameConst.TWEENT_INTER_MAP, False)
        self.add("hideInterMap", False)
        self.add("virtualPlayerJump", False)
        self.add("reloadLoadedMap", False)
        self.add("hideForeground", False)
        self.add("allowAnimatedGfx", True)
        self.add("allowParticlesFx", True)
        self.add("elementsPath")
        self.add("swfPath")
        self.add("mapsPath")
        self.add("elementsIndexPath")
        self.add("transparentOverlayMode", False)
        self.add("groundOnly", False)
        self.add("showTransitions", False)
        self.add("useLowDefSkin", True)
        self.add("showProgressBar", False)
        self.add("hideBlackBorder", True)
        self.add("tacticalModeTemplatesPath")
        self.add("useWorldEntityPool", False)

