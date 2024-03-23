import threading
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementCancelMessage import GameMapMovementCancelMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import \
        AnimatedCharacter
    from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import \
        MovementPath
class MovementBehavior(threading.Thread):
    
    def __init__(self, clientMovePath: 'MovementPath', callback, parent: 'AnimatedCharacter'=None):
        super().__init__(name=threading.currentThread().name)
        self.parent = parent
        self.movePath = clientMovePath
        self.currStep = self.movePath.path[0]
        self.stopEvt = threading.Event()
        self.running = threading.Event()
        self.callback = callback
        
    def stop(self, callback=None):
        self.stopEvt.set()

    def isRunning(self):
        return self.running.is_set()

    def tearDown(self, success):
        from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler

        if not success:
            Logger().warning(f"Movement animation interrupted")
            if PlayedCharacterManager().isFighting:
                return
            msg = GameMapMovementCancelMessage()
            msg.init(self.currStep.cellId)
            ConnectionsHandler().send(msg)
        else:
            Logger().info(f"Movement animation completed")
        self.parent.isMoving = False
        self.running.clear()
        return self.callback(success)

    def run(self):
        Logger().info(f"Movement animation started")
        self.parent.isMoving = True
        self.running.set()
        for pe in self.movePath.path[1:] + [self.movePath.end]:
            stepDuration = self.movePath.getStepDuration(self.currStep.orientation)
            if not self.parent.isMoving:
                Logger().info(f"Movement animation detected player not moving")
                return self.tearDown(False)
            if self.stopEvt.wait(stepDuration):
                Logger().info(f"Movement animation received stop event")
                return self.tearDown(False)
            self.currStep = pe
        self.tearDown(True)

