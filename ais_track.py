from typing import List

from pydantic import BaseModel


class AISTrack(BaseModel):
    mmsi: int
    nav_status: int
    lon: float
    lat: float
    speed: float
    course: float
    imo: int
    call_sign: str
    ship_name: str
    ship_type: int
    dimension: dict
    eta: dict
    draught: float
    destination: str

    def generate_nmea(self):
        pass


class AISTrackList(BaseModel):
    tracks: List[AISTrack]