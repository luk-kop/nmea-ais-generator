from typing import List
import socket
import time
import sys
import threading

from ais_utils import Clients


class UDPStream:
    """
    Class represents a stream of UDP data sent to selected hosts.
    """
    def __init__(self, clients: Clients) -> None:
        self.clients_list = clients
        self.data_to_send = []

    def run(self, data: List[str]) -> None:
        """
        Starts UDP stream tx.
        """
        self.data_to_send = data
        for client in self.clients_list.clients:
            host, port = client.host, client.port
            # Send data to each host:port in a separate thread
            threading.Thread(target=self.send_data,
                             kwargs={'host': host, 'port': port},
                             name=f'ais_thread_{host}:{port}').start()

    def send_data(self, host: str, port: int) -> None:
        """
        Sends UDP data stream to specified host:port pair.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            for nmea in self.data_to_send:
                try:
                    s.sendto(nmea.encode(), (host, port))
                    time.sleep(0.05)
                except OSError as err:
                    print(f'Error: {err.strerror}')
                    sys.exit()
