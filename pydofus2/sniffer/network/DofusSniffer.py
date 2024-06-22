#!/usr/bin/python
import asyncio
import base64
import os
import threading

import pyshark
from pyshark.tshark.tshark import get_process_path, get_tshark_interfaces

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

from .DofusConnection import LOCAL_IP, ConnEvent, DofusConnection
from .Packet import TCPPacket

# Global variables for message storage and sniffer control
messages_lock = threading.Lock()
LOW_LEVEL_DEBUG = bool(os.environ.get("LOW_LEVEL_DEBUG", False))


class DofusSniffer(threading.Thread):
    def __init__(self, name="DofusSnifferApp", on_message=None, on_crash=None, recordMessages=True):
        super().__init__(name=name)
        self.capture = None
        self.connections = dict[int, DofusConnection]()
        self.callback = on_message
        self.recordMessages = recordMessages
        self.messagesRecord = {}
        self.running = threading.Event()
        self.on_crash = on_crash
        self._stoped = False

    def process_packet(self, p):
        if not self.running.is_set():
            self.running.set()
        try:
            p = TCPPacket(p)
            if LOW_LEVEL_DEBUG:
                Logger().debug(f"Received packet: {p}")
            local_port = p.srcport if p.src == LOCAL_IP else p.dstport
            conn = self.connections.get(local_port)
            if not conn:
                conn = DofusConnection.initFromPacket(p)
                if not conn:
                    return
                self.messagesRecord[conn.id] = []
                conn.handle = self.handle
                self.connections[local_port] = conn
                conn.on(ConnEvent.CLOSE, lambda _, conn_id: self.connections.pop(conn_id))
            conn.low_receive(p)
        except Exception as e:
            Logger().error(f"Error while handling {p.all_fields()}: {e}", exc_info=True)
            self.stop()

    def handle(self, conn: DofusConnection, msg: NetworkMessage, from_client: bool):
        if msg.unpacked:
            if self.recordMessages:
                msgjson = msg.to_json()
                msgjson["__receptionTime__"] = msg.receptionTime
                msgjson["__direction__"] = "snd" if from_client else "rcv"
                if "hash_function" in msgjson:
                    msgjson["hash_function"] = base64.b64encode(msgjson["hash_function"]).decode("utf-8")
                with messages_lock:
                    self.messagesRecord[conn.id].append(msgjson)
                    # with open(conn.messagesRecordFile, "w") as fp:
                    #     json.dump(self.messagesRecord[conn.id], fp, indent=2)
            if self.callback:
                self.callback(conn.id, msg, from_client)

    def run(self):
        Logger().debug("Started sniffer")
        tshark_path = get_process_path()
        interfaces = get_tshark_interfaces(tshark_path)
        Logger().debug(f"Available interfaces: {interfaces}")
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.capture = pyshark.LiveCapture(bpf_filter="tcp port 5555")
            self.running.set()
            self.loop.run_until_complete(self.capture.packets_from_tshark(self.process_packet))
            self.running.clear()
        except Exception as e:
            if self._stoped:
                return
            import sys
            import traceback

            Logger().error(f"Error in sniffer thread: {e}", exc_info=True)
            _, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            # Start with the current exception's traceback
            error_trace = "\n".join(traceback_in_var) + "\n" + str(exc_value)
            # Check for and add traceback from the cause, if any
            cause = e.__cause__
            while cause:
                cause_traceback = traceback.format_tb(cause.__traceback__)
                error_trace += "\n\n-- Chained Exception --\n"
                error_trace += "\n".join(cause_traceback) + "\n" + str(cause)
                cause = cause.__cause__
            Logger().debug("Stopped sniffer")
            self.running.clear()
            if self.on_crash:
                self.on_crash(error_trace)

    def stop(self):
        self._stoped = True
        self.loop.create_task(self.capture.close_async())


if __name__ == "__main__":
    mySniffer = DofusSniffer()
    mySniffer.start()
    try:
        mySniffer.start()
    except KeyboardInterrupt:
        mySniffer.stop()
