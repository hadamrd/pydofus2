
import random
import string
from time import perf_counter
from typing import List

from pydofus2.sniffer.network.Packet import TCPPacket
from pydofus2.sniffer.network.SnifferBuffer import SnifferBuffer


def generate_test_data(size: int = 10000024, chunk_size_range=(1000, 10000)) -> List[TCPPacket]:
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    packets = []

    start_seq = 0
    while start_seq < len(data):
        chunk_size = random.randint(*chunk_size_range)
        end_seq = min(start_seq + chunk_size, len(data))
        packet_data = data[start_seq:end_seq].encode()
        packets.append(TCPPacket(None, True, start_seq, packet_data))
        start_seq += chunk_size

    first_packet = packets.pop(0)
    random.shuffle(packets)
    packets.insert(0, first_packet)

    return packets, data.encode()

def test_sniffer_buffer():
    buffer = SnifferBuffer()
    test_packets, data = generate_test_data()

    t = perf_counter()
    for packet in test_packets:
        buffer.write(packet)
    print(f"Time elapsed: {perf_counter() - t}")
    
    reconstructed_data = buffer.read()
    assert reconstructed_data == data, \
        f"Reconstructed data does not match original data: {reconstructed_data} != {data}"

    print("Test passed!")

test_sniffer_buffer()
