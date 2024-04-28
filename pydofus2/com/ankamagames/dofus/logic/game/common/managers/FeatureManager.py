from threading import Lock
from types import FunctionType

from pydofus2.com.ankamagames.dofus.datacenter.feature.OptionalFeature import OptionalFeature
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton

lock = Lock()


class FeatureManager(metaclass=ThreadSharedSingleton):
    def __init__(self):
        super().__init__()
        Logger().info("Instantiating feature manager")
        self._enabledFeatureIds = list[int]()
        self._featureListeners = dict()
        self._featureListeners = dict()

    @property
    def enabledFeatureIds(self) -> list[int]:
        return self._enabledFeatureIds

    def resetEnabledFeatures(self) -> None:
        Logger().info("Resetting enabled features")
        with lock:
            self._enabledFeatureIds = list[int]()

    def resetEnabledServerFeatures(self) -> None:
        Logger().info("Resetting enabled server features")
        featureId: int = -1
        feature: OptionalFeature = None
        index: int = 0
        while index < len(self._enabledFeatureIds):
            featureId = self._enabledFeatureIds[index]
            feature = OptionalFeature.getOptionalFeatureById(featureId)
            if feature == None:
                Logger().error(
                    "Feature with ID " + str(featureId) + " is enabled AND None. What happened? Disabling it"
                )
                with lock:
                    del self._enabledFeatureIds[index]
            elif feature.isServer:
                self.disableFeature(feature)
            else:
                index += 1

    def resetEnabledServerConnectionFeatures(self) -> None:
        Logger().info("Resetting enabled server-connection features")
        featureId: int = -1
        feature: OptionalFeature = None
        index: int = 0
        while index < len(self._enabledFeatureIds):
            featureId = self._enabledFeatureIds[index]
            feature = OptionalFeature.getOptionalFeatureById(featureId)
            if feature is None:
                Logger().error(
                    "Feature with ID " + str(featureId) + " is enabled AND None. What happened? Disabling it"
                )
                with lock:
                    del self._enabledFeatureIds[index]
            elif feature.isClient and not feature.isServer and feature.isActivationOnServerConnection:
                self.disableFeature(feature)
            else:
                index += 1

    def isFeatureWithIdEnabled(self, featureId: int) -> bool:
        return featureId in self._enabledFeatureIds

    def isFeatureWithKeywordEnabled(self, featureKeyword: str) -> bool:
        feature: OptionalFeature = OptionalFeature.getOptionalFeatureByKeyword(featureKeyword)
        if feature == None:
            Logger().error(
                "Tried to enable non-existing feature (keyword: "
                + featureKeyword
                + "). Is self an export issue? Aborting"
            )
            return False
        return self.isFeatureEnabled(feature)

    def isFeatureEnabled(self, feature: OptionalFeature) -> bool:
        if feature == None:
            Logger().error("Feature instance to check is None")
            return False
        return feature.id in self._enabledFeatureIds

    def enableFeatureWithId(self, featureId: int, isForce: bool = False) -> bool:
        feature: OptionalFeature = OptionalFeature.getOptionalFeatureById(featureId)
        if feature == None:
            Logger().error(
                "Tried to enable non-existing feature (ID: " + str(featureId) + "). Is self an export issue? Aborting"
            )
            return False
        return self.enableFeature(feature, isForce)

    def enableFeatureWithKeyword(self, featureKeyword: str, isForce: bool = False) -> bool:
        feature: OptionalFeature = OptionalFeature.getOptionalFeatureByKeyword(featureKeyword)
        if feature == None:
            Logger().error(
                "Tried to enable non-existing feature (keyword: "
                + featureKeyword
                + "). Is self an export issue? Aborting"
            )
            return False
        return self.enableFeature(feature, isForce)

    def enableFeature(self, feature: OptionalFeature, isForce: bool = False) -> bool:
        if feature == None:
            Logger().error("Feature instance to enable is None")
            return False
        if self.isFeatureEnabled(feature):
            str(Logger().warn(feature) + " already enabled")
            return False
        if not feature.isClient:
            if not isForce:
                Logger().error("Cannot enable non-client feature (" + str(feature) + "). Aborting")
                return False
            Logger().warn("Enabling non-client feature (" + str(feature) + "). But the FORCE flag has been set")
        if not feature.canBeEnabled:
            if not isForce:
                Logger().error("Feature CANNOT be enabled (" + str(feature) + "). Aborting")
                return False
            Logger().warn("Feature cannot normally be enabled (" + str(feature) + "). But the FORCE flag has been set")
        with lock:
            self._enabledFeatureIds.append(feature.id)
        str(Logger().info(feature) + " enabled")
        self.fireFeatureActivationUpdate(feature, True)
        return True

    def disableFeatureWithId(self, featureId: int) -> bool:
        featureIdLabel: str = None
        feature: OptionalFeature = OptionalFeature.getOptionalFeatureById(featureId)
        if feature == None:
            featureIdLabel = str(featureId)
            Logger().error(f"Tried to disable non-existing feature (ID: {featureIdLabel}). Is self an export issue?")
            if featureId in self._enabledFeatureIds:
                Logger().warn(f"Yet non-existing feature (ID: {featureIdLabel}) is enabled... Disabling it")
                with lock:
                    self._enabledFeatureIds.remove(featureId)
                Logger().warn(f"Non-existing feature (ID: {featureIdLabel}) disabled")
            else:
                Logger().warn(f"Non-existing feature (ID: {featureIdLabel}) is not enabled anyway")
            return False
        return self.disableFeature(feature)

    def disableFeatureWithKeyword(self, featureKeyword: str) -> bool:
        feature: OptionalFeature = OptionalFeature.getOptionalFeatureByKeyword(featureKeyword)
        if feature == None:
            Logger().error(
                "Tried to disable non-existing feature (keyword: "
                + featureKeyword
                + "). Is self an export issue? Aborting"
            )
            return False
        return self.disableFeature(feature)

    def disableFeature(self, feature: OptionalFeature) -> bool:
        if feature == None:
            Logger().error("Feature instance to disable is None")
            return False
        featureIdIndex: float = self._enabledFeatureIds.index(feature.id)
        if featureIdIndex == -1:
            str(Logger().warn(feature) + " already disabled")
            return False
        with lock:
            del self._enabledFeatureIds[featureIdIndex]
        str(Logger().info(feature) + " disabled")
        self.fireFeatureActivationUpdate(feature, False)
        return True

    def getEnabledFeatureKeywords(self) -> list[str]:
        enabledFeatureKeywords: list[str] = list[str]()
        for featureId in self._enabledFeatureIds:
            feature = OptionalFeature.getOptionalFeatureById(featureId)
            if feature is not None:
                enabledFeatureKeywords.append(feature.keyword)
            else:
                enabledFeatureKeywords.append(None)
        return enabledFeatureKeywords

    def getEnabledFeatures(self) -> list[OptionalFeature]:
        featureId: int = 0
        enabledFeatures: list[OptionalFeature] = list[OptionalFeature]()
        for featureId in self._enabledFeatureIds:
            enabledFeatures.append(OptionalFeature.getOptionalFeatureById(featureId))
        return enabledFeatures

    def getDisabledFeatureIds(self) -> list[int]:
        optionalFeatures: list = OptionalFeature.getAllOptionalFeatures()
        disabledFeatureIds: list[int] = list[int]()
        for optionalFeature in optionalFeatures:
            if optionalFeature is not None and optionalFeature.id not in self._enabledFeatureIds:
                disabledFeatureIds.append(optionalFeature.id)
        return disabledFeatureIds

    def getDisabledFeatureKeywords(self) -> list[str]:
        optionalFeature: OptionalFeature = None
        optionalFeatures: list = OptionalFeature.getAllOptionalFeatures()
        disabledFeatureKeywords: list[str] = list[str]()
        for optionalFeature in optionalFeatures:
            if optionalFeature is not None and optionalFeature.id not in self._enabledFeatureIds:
                disabledFeatureKeywords.append(optionalFeature.keyword)
        return disabledFeatureKeywords

    def getDisabledFeatures(self) -> list[OptionalFeature]:
        optionalFeature: OptionalFeature = None
        optionalFeatures: list = OptionalFeature.getAllOptionalFeatures()
        disabledFeatures: list[OptionalFeature] = list[OptionalFeature]()
        for optionalFeature in optionalFeatures:
            if optionalFeature is not None and optionalFeature.id not in self._enabledFeatureIds:
                disabledFeatures.append(optionalFeature)
        return disabledFeatures

    def isFeatureHasListener(self, feature: OptionalFeature, listener: FunctionType) -> bool:
        return self.getFeatureListenerIndex(feature, listener) != -1

    def getFeatureListenerIndex(self, feature: OptionalFeature, listener: FunctionType) -> float:
        listeners: list[FunctionType] = self._featureListeners.get(feature.id)
        if listeners is None:
            return -1
        if len(listeners) <= 0:
            del self._featureListeners[feature.id]
            return -1
        if listener in listeners:
            return listeners.index(listener)
        return -1

    def fireFeatureActivationUpdate(self, feature: OptionalFeature, isEnabled: bool) -> None:
        listeners: list[FunctionType] = self._featureListeners[feature.id]
        if listeners == None:
            return
        currentListener: FunctionType = None
        index: int = 0
        while index < len(listeners):
            currentListener = listeners[index]
            currentListener.call(None, feature.keyword, feature.id, isEnabled)
            index += 1
        if len(listeners) <= 0:
            del self._featureListeners[feature.id]
