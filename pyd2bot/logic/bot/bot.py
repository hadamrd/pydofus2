import logging
logger = logging.getLogger("bot")
import threading
from time import sleep
import pyautogui
from pyd2bot.network.message import Msg
from pyd2bot.network.sniffer import DofusSniffer 

class Bot(threading.Thread):

    def __init__(self, workdir, name="Bot"):
        super(Bot, self).__init__(name=name)
        self.inventoryWeight = None
        self.weightMax = None
        self.killsig = threading.Event()
        self.lock = threading.Lock()
        self.disconnected = threading.Event()
        self.connected = threading.Event()
        self.moving = threading.Event()
        self.idle = threading.Event()
        self.fullPods = threading.Event()
        self.fullPodsAAA = threading.Event()
        self.name = name
        self.dead = False
        self.workdir = workdir
        self.resourcesToFarm = []
        self.sniffer = DofusSniffer(self.handleMsg)
        self.currMapData = None
        self.currMapInteractiveElems = {}
        self.currMapStatedElems = {}
        self.id = {}
        self.context = 1
        
    def interrupt(self):
        self.killsig.set()
        try:
            self.sniffer.stop()
        except:
            logger.error("Fatal error in interrupt!", exc_info=True)
        logger.info('Goodbye cruel world.')
        
    @staticmethod
    def shiftClick(tgt):
        pyautogui.keyDown('shift')
        sleep(0.1)
        tgt.click()
        sleep(0.1)
        pyautogui.keyUp('shift')
        dofus.OUT_OF_COMBAT_R.hover()

    def harvest(self):
        pass

    @staticmethod
    def checkPopup():
        m = dofus.LVL_UP_INFO_R.find(dofus.CLOSE_POPUP_P)
        if m:
            m.click()

    def handleMsg(self, msg: Msg):
        logger.info("received msg: " + msg.msgName["name"])     
        if msg.msgName["name"] == "InventoryWeightMessage":
            msg_json = msg.json()
            self.inventoryWeight = msg_json["inventoryWeight"]
            self.weightMax = msg_json["weightMax"]
            prcnt = self.inventoryWeight / self.weightMax
            if prcnt > 0.9:
                logger.info(f"Bot reached {100 * prcnt} of pod available")
                self.fullPodsAAA.set()
            
        if msg.msgName["name"] == "NotificationUpdateFlagMessage":
            msg_json = msg.json()
            if msg_json["index"] == 37:
                self.fullPods.set()
                logger.info("Got bot full pod notif from server")
        
        if msg.msgName["name"] == "GameContextCreateMessage":
            msg_json = msg.json()
            self.context = msg_json["context"]
        
            