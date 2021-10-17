from typing import List, Dict
import socket
import time
import sys


class UDPStream:
    """
    Class represents a stream of UDP data sent to selected hosts.
    """
    def __init__(self, clients: Dict[str, int]):
        self.clients = clients

    def send(self, data: List[str]):
        for ip_address, port in self.clients.items():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                for nmea in data:
                    try:
                        s.sendto(nmea.encode(), (ip_address, port))
                        time.sleep(0.05)
                    except OSError as err:
                        print(f'Error: {err.strerror}')
                        sys.exit()
