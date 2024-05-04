from queue import Queue

from PyQt5.QtCore import QMutex, QMutexLocker, QObject, QRunnable, QThreadPool, QWaitCondition, pyqtSignal

from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.PakProtocol2 import PakProtocol2
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class GfxLoaderWorker(QRunnable):
    def __init__(
        self, task_queue: Queue, mutex: QMutex, init_conditions: dict[str, QWaitCondition], loader: "GfxParallelLoader"
    ):
        super().__init__()
        self.task_queue = task_queue
        self.mutex = mutex
        self.loader = loader
        self.init_conditions = init_conditions

    def run(self):
        with QMutexLocker(self.mutex):
            self.loader.active_workers += 1

        while True:
            uri: Uri = None
            with QMutexLocker(self.mutex):
                if self.task_queue.empty():
                    break
                uri = self.task_queue.get()

            if uri:
                try:
                    # Check and wait if initialization is needed and ongoing by another thread
                    self.wait_for_initialization(uri.path)

                    # Perform the initialization if needed
                    if uri.path not in self.loader.protocol.indexes:
                        with QMutexLocker(self.mutex):
                            # Check again to ensure it hasn't been initialized in the meantime
                            if uri.path not in self.loader.protocol.indexes:
                                self.init_conditions[uri.path] = QWaitCondition()
                                self.loader.protocol.initStreamsIndexTable(uri)
                                condition = self.init_conditions.pop(uri.path, None)
                                if condition:
                                    condition.wakeAll()

                    # Load directly after ensuring the initialization is done
                    result = self.loader.protocol.loadDirectly(uri)
                    if result is None:
                        raise Exception(
                            f"No GFX found matching the uri {uri.path} / {uri.subPath} in the gfx d2o file index"
                        )

                    self.loader.progress.emit(uri.tag, result)

                except Exception as e:
                    self.loader.error.emit(uri.tag, str(e))
        with QMutexLocker(self.mutex):
            self.loader.active_workers -= 1
        self.loader.onWorkerDied()

    def wait_for_initialization(self, path):
        with QMutexLocker(self.mutex):
            if path in self.loader.protocol._indexes:
                return  # Already initialized, no need to wait
            if path in self.init_conditions:
                condition = self.init_conditions[path]
                condition.wait(self.mutex)  # Wait until initialization is complete


class GfxParallelLoader(QObject):
    progress = pyqtSignal(int, bytes)  # Emit tag and result
    error = pyqtSignal(int, Exception)  # Emit error message
    finished = pyqtSignal()  # Emit when all tasks are done

    def __init__(self, maxThreads=6):
        super().__init__()
        self.task_queue = Queue()
        self.mutex = QMutex()
        self.pool = QThreadPool()
        self.protocol = PakProtocol2()
        self.pool.setMaxThreadCount(maxThreads)
        self.active_workers = 0
        self.init_conditions = {}

    def loadItems(self, uris: list[Uri]):
        for uri in uris:
            self.task_queue.put(uri)
        if not self.pool.activeThreadCount():
            for _ in range(self.pool.maxThreadCount()):
                worker = GfxLoaderWorker(self.task_queue, self.mutex, self.init_conditions, self)
                self.pool.start(worker)

    def onWorkerDied(self):
        if self.active_workers == 0:
            self.finished.emit()
