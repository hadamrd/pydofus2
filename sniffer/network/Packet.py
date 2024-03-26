from pyshark.packet.layers.base import BaseLayer

from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray


class TCPPacket:

    def __init__(self, tcp_packet, mock=False, seq=None, data=None):
        if mock:
            self.seq = seq
            self.nxtseq = seq + len(data)
            self.data = data
            return

        if isinstance(tcp_packet.tcp, BaseLayer):
            self.ack = int(tcp_packet.tcp.ack)
            self.seq = int(tcp_packet.tcp.seq)
            self.nxtseq = int(tcp_packet.tcp.nxtseq)
            self.len = int(tcp_packet.tcp.len)
            self.src = tcp_packet.ip.src
            self.dst = tcp_packet.ip.dst
            self.srcport = int(tcp_packet.tcp.srcport)
            self.dstport = int(tcp_packet.tcp.dstport)
            self.flags = tcp_packet.tcp.flags
            self.flags_syn = int(tcp_packet.tcp.flags_syn)
            self.flags_ack = int(tcp_packet.tcp.flags_ack)
            self.flags_fin = int(tcp_packet.tcp.flags_fin)
            self.flags_reset = int(tcp_packet.tcp.flags_reset)
            self.flags_push = int(tcp_packet.tcp.flags_push)
            self.connection_syn = tcp_packet.tcp.get_field("tcp.connection.syn")
            self.connection_synack = tcp_packet.tcp.get_field("tcp.connection.synack")
            self._all_fields = tcp_packet.tcp._all_fields
            payload = tcp_packet.tcp.get_field("tcp.payload")
            self.data = ByteArray(payload.binary_value if payload else b"")
        else:
            raise ValueError("Invalid packet")

    def all_fields(self):
        return self._all_fields

    def __lt__(self, other: "TCPPacket"):
        return self.seq < other.seq

    def __add__(self, other: "TCPPacket"):
        if self.nxtseq != other.seq:
            raise Exception("Invalid packet operation")
        return TCPPacket(self.seq, self.data + other.data)

    def __repr__(self) -> str:
        return f"P(seq={self.seq}, nxtseq={self.nxtseq}, len={len(self.data)})"

    def rappend(self, other: "TCPPacket"):
        if self.nxtseq != other.seq:
            raise Exception("Invalid packet operation")
        self.nxtseq = other.nxtseq
        self.data += other.data

    def lappend(self, other: "TCPPacket"):
        if other.nxtseq != self.seq:
            raise Exception("Invalid packet operation")
        self.seq = other.seq
        self.data = other.data + self.data
