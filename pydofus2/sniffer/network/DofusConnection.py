import datetime
import os
import socket
from types import FunctionType

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event, EventsHandler
from pydofus2.com.ankamagames.dofus.network.MessageReceiver import MessageReceiver
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

from .Packet import TCPPacket
from .SnifferBuffer import SnifferBuffer

LOW_LEVEL_DEBUG = os.environ.get("LOW_LEVEL_DEBUG", False)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


LOCAL_IP = get_ip()


class ConnEvent(Event):
    SERVER_PACKET = "server_packet"
    CLIENT_PACKET = "client_packet"
    CLOSE = "close"

    def __init__(self, conn_id, data={}) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.data = data


class ConnState:
    FIN = -1
    SYN = 0  # SYN_SENT
    SYN_ACK = 1  # SYN-ACK_RECEIVED
    ESTABLISHED = 2  # ESTABLISHED


class DofusConnection(EventsHandler):
    server_ip: str
    client_ip: str
    clientBuffer: SnifferBuffer
    serverBuffer: SnifferBuffer
    state: ConnState
    server_port: int
    client_port: int
    defaultHandle: FunctionType
    handle: FunctionType
    currPlayerId: int

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.state = None
        self.messagesCount = 0
        self.messagesRecordFile = None
        self.handle = None

    @classmethod
    def initFromPacket(cls, p: TCPPacket) -> "DofusConnection":
        instance = cls(None)
        if p.flags_fin or (p.seq != 0 and p.flags_ack and p.len < 1):
            if LOW_LEVEL_DEBUG:
                Logger().warning(f"Can't init a connection from FIN or ack packet.")
            return None
        if p.src == LOCAL_IP:
            instance.server_ip = p.dst
            instance.server_port = p.dstport
            instance.client_ip = p.src
            instance.client_port = p.srcport
        else:
            instance.server_ip = p.src
            instance.server_port = p.srcport
            instance.client_ip = p.dst
            instance.client_port = p.dstport
        instance.id = f"client:{instance.client_ip}:{instance.client_port} <-> server:{instance.server_ip}:{instance.server_port}"
        instance.clientBuffer = SnifferBuffer(id="Client Buffer")
        instance.serverBuffer = SnifferBuffer(id="Server Buffer")
        instance.state = None
        instance.messagesRecordFile = f"client_{instance.client_ip}_{instance.client_port}_record.json"
        Logger().debug(
            f"Created new connection '{instance.id}', localIp {LOCAL_IP}, packet src {p.src}:{p.srcport}, packet dest {p.dst}:{p.dstport}"
        )
        return instance

    def low_receive(self, p: TCPPacket):
        if p.flags_syn:
            if p.flags_ack:
                self.state = ConnState.SYN_ACK
                Logger().debug(f"[{self.id}] {p.connection_synack}")
            else:
                self.state = ConnState.SYN
                Logger().debug(f"[{self.id}] {p.connection_syn}")
        elif p.flags_fin:
            if p.src == LOCAL_IP:
                Logger().debug(f"[{self.id}] Connection closed by client")
            else:
                Logger().debug(f"[{self.id}] Connection closed by server")
            self.state = ConnState.FIN
            self.send(ConnEvent.CLOSE, self.client_port)
            return
        elif p.flags_reset:
            self.clientBuffer.clear()
            self.serverBuffer.clear()
        elif p.flags_ack and p.len < 1 and self.state is None:
            self.state = ConnState.ESTABLISHED
        else:
            if self.state is None:
                Logger().debug(f"[{self.id}] Connection established")
                self.state = ConnState.ESTABLISHED
            self.onPacket(p)

    def onMessageParsed(self, msg: NetworkMessage, from_client: bool):
        msg.receptionTime = datetime.datetime.now().strftime("%H:%M:%S:%f")
        msg.sourceConnection = self.id
        if type(msg).__name__ == "NetworkDataContainerMessage":
            Logger().debug(f"Received network Datacontainer with content of size : {len(msg.content)}")
            MessageReceiver(False).parse(ByteArray(msg.content), self.onMessageParsed, from_dataContainer=True)
        else:
            self.handle(self, msg, from_client)

    def onPacket(self, p: TCPPacket):
        from_client = p.src == LOCAL_IP
        buffer = self.clientBuffer if from_client else self.serverBuffer
        buffer.write(p)
        if self.handle is None:
            self.handle = lambda conn, msg, from_client: None
        try:
            MessageReceiver(False).parse(
                buffer.read(), lambda msg, from_client: self.onMessageParsed(msg, from_client), from_client
            )
        except Exception as e:
            buffer.trim()
            Logger().warning(e)
