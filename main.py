from pathlib import Path
from typing import Dict, List, Any
import json
import sys
import time
from datetime import datetime
import argparse

from pydantic import ValidationError

from ais_track import AISTrackList
from ais_utils import Clients, Client
from nmea_stream import UDPStream


class AISDataTx:
    """
    Class represents generated AIS data for clients (customers).
    The AIS data is sent as UDP packets to clients in NMEA 0183 format and optionally can be displayed on CLI terminal.
    """
    def __init__(self, tracks_file: str = 'tracks.json', terminal_output: bool = False, new_tracks_file: str = ''):
        self.tracks_file = tracks_file
        self.clients_file = 'clients.json'
        self.track_list = None
        self.clients = None
        self.terminal_output = terminal_output
        # Save current AIS tracks data to new JSON file
        self.new_tracks_file = new_tracks_file

    def load_files(self) -> None:
        """
        Loads clients and AIS tracks from JSON files.
        """
        try:
            # Load clients_file
            file_name = self.clients_file
            clients_list = Clients.parse_file(Path(file_name))
            # Load tracks_file
            file_name = self.tracks_file
            track_list = AISTrackList.parse_file(Path(file_name))
            self.clients = clients_list
            self.track_list = track_list
            return
        except FileNotFoundError:
            print(f'Error: File {file_name} does not exist!')
        except json.decoder.JSONDecodeError as error:
            print(f'Error: File {file_name} - {error}')
        except ValidationError as error:
            # Custom error msg
            error_data: List[Dict[str, Any]] = error.errors()
            error_msg: str = error_data[0]['msg']
            item_no: int = error_data[0]['loc'][1] + 1
            item_field: str = error_data[0]['loc'][-1]
            print(f'Error: File "{file_name}" - check item with no {item_no}, "{item_field}" {error_msg}')
        sys.exit()

    def run(self, timer: int = 30):
        """
        Starts the process of sending AIS tracks data to selected hosts.
        """
        self.load_files()
        udp = UDPStream(clients=self.clients)
        print('Press "Ctrl + c" to exit\n')
        print(f'Sending NMEA AIS data via UDP stream...\n')
        if self.terminal_output:
            print('NMEA AIS data output:')
        while True:
            try:
                timer_start = time.perf_counter()
                nmea_msgs = []
                for track in self.track_list.tracks:
                    # Update AIS track position with each while loop run
                    current_timestamp = datetime.utcnow().timestamp()
                    if track.speed > 0:
                        # Updated only if track in move
                        track.update_position(current_timestamp=current_timestamp)
                    nmea_msgs += track.generate_nmea()
                # Send UDP packets with NMEA data
                udp.run(data=nmea_msgs)
                # Print NMEA dat to terminal output
                if self.terminal_output:
                    for msg in nmea_msgs:
                        print(msg, end='')
                        time.sleep(0.02)
                time.sleep(timer - (time.perf_counter() - timer_start))
            except KeyboardInterrupt:
                new_tracks_file = self.new_tracks_file
                if new_tracks_file:
                    print(f'\nSaving AIS data to "{new_tracks_file}" file...')
                    self.save_tracks_to_new_file(filename=new_tracks_file)
                print('\nClosing the script...\n')
                sys.exit()

    def save_tracks_to_new_file(self, filename: str):
        """
        Dumps AIS tracks to new JSON file.
        """
        path = Path(filename)
        if self.new_tracks_file and self.track_list:
            # Convert AISTrackList model to dictionary & exclude not set fields or with default values
            tracks: List[Dict] = self.track_list.dict(exclude_unset=True)['tracks']
            # Strip selected AIS track attrs (model fields) values
            for track in tracks:
                values_to_strip = ['ship_name', 'destination', 'call_sign']
                for string in values_to_strip:
                    track[string] = track[string].strip()
            # Dump data as a dict
            tracks_to_dump = {
                'tracks': tracks
            }
            with open(path, 'w') as write_file:
                json.dump(tracks_to_dump, write_file, indent=4)


if __name__ == '__main__':
    default_timer = 15

    parser = argparse.ArgumentParser(description='The script generates NMEA AIS data')
    parser.add_argument('-f', '--filename', default='tracks.json', type=str,
                        help='JSON file with AIS tracks (default: tracks.json)')
    parser.add_argument('-s', '--save', type=str, help='Save generated NMEA data to new JSON file')
    parser.add_argument('-o', '--output', action="store_true", help='Print NMEA data on terminal output')
    args = parser.parse_args()

    # Get data from argparse
    ais_class_attr = {}
    if args.filename:
        ais_class_attr['tracks_file'] = args.filename
    if args.save:
        ais_class_attr['new_tracks_file'] = args.save
    if args.output:
        ais_class_attr['terminal_output'] = args.output
    # Run AIS emulator
    AISDataTx(**ais_class_attr).run(timer=default_timer)