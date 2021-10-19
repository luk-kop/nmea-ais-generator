from pathlib import Path
from typing import Dict, List, Any
import json
import sys
import time

from pydantic import ValidationError

from ais_track import AISTrackList
from nmea_stream import UDPStream


class AISDataTx:
    def __init__(self, tracks_data_file: str = 'tracks.json', save_tracks_data: bool = False):
        self.tracks_file = tracks_data_file
        self.track_list = None
        # Save current AIS tracks data to new JSON file
        self.save_tracks_data = save_tracks_data

    def load_tracks_from_file(self) -> None:
        """
        Loads AIS tracks from JSON file.
        """
        path = Path(self.tracks_file)
        try:
            track_list = AISTrackList.parse_file(path)
            self.track_list = track_list
            return
        except FileNotFoundError:
            print(f'Error: File {self.tracks_file} does not exist!')
        except json.decoder.JSONDecodeError as error:
            print(f'Error: File {self.tracks_file} - {error}')
        except ValidationError as error:
            # Custom error msg
            error_data: List[Dict[str, Any]] = error.errors()
            error_msg: str = error_data[0]['msg']
            track_no: int = error_data[0]['loc'][1] + 1
            track_field: str = error_data[0]['loc'][-1]
            print(f'Error: File "{self.tracks_file}" - check track with no {track_no}, "{track_field}" {error_msg}')
        sys.exit()

    def run(self, clients: Dict[str, int], timer: int = 30):
        """
        Starts the process of sending AIS tracks data to selected hosts.
        """
        self.load_tracks_from_file()
        udp = UDPStream(clients=clients)
        print('Press "Ctrl + c" to exit\n')
        print(f'Sending NMEA AIS data...')
        while True:
            try:
                timer_start = time.perf_counter()
                nmea_msgs = []
                for track in self.track_list.tracks:
                    # track.update_position()
                    nmea_msgs += track.generate_nmea()
                udp.run(data=nmea_msgs)
                time.sleep(timer - (time.perf_counter() - timer_start))
            except KeyboardInterrupt:
                print('\nClosing the script...\n')
                sys.exit()

    def save_tracks_to_new_file(self, filename: str):
        """
        Dumps AIS tracks to new JSON file.
        """
        path = Path(filename)
        if self.save_tracks_data and self.track_list:
            # Strip selected AIS track attrs values
            tracks = self.track_list.dict()['tracks']
            for track in tracks:
                values_to_strip = ['ship_name', 'destination', 'call_sign']
                for string in values_to_strip:
                    track[string] = track[string].strip()
            with open(path, 'w') as write_file:
                json.dump(tracks, write_file, indent=4)


if __name__ == '__main__':
    clients = [
        {
            'host': '127.0.0.1',
            'port': 1111
        },
        {
            'host': '127.0.0.1',
            'port': 1112
        },
        {
            'host': '127.0.0.1',
            'port': 1113
        },
        {
            'host': '172.16.208.131',
            'port': 1002
        },
    ]

    AISDataTx().run(clients=clients, timer=20)