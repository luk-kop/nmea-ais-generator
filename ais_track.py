from typing import List

from pydantic import BaseModel, validator

from nmea_utils import convert_int_to_bits


class ShipDimension(BaseModel):
    """
    Class represents the dimension of the ship. All dimensions in meters.
    """
    to_bow: int = 0
    to_stern: int = 0
    to_port: int = 0
    to_starboard: int = 0

    class Config:
        validate_assignment = True

    @validator('to_bow', 'to_stern')
    def check_to_bow_and_to_stern_value(cls, value, field):
        if value < 0:
            raise ValueError(f'Invalid {field.name} {value}. Should be 0 or greater.')
        elif value > 511:
            value = 511
        return value

    @validator('to_port', 'to_starboard')
    def check_to_port_and_to_starboard_value(cls, value, field):
        if value < 0:
            raise ValueError(f'Invalid {field.name} {value}. Should be 0 or greater.')
        elif value > 63:
            value = 63
        return value

    @property
    def bits(self) -> str:
        dimension_bits = ''
        for value in [self.to_bow, self.to_stern]:
            dimension_bits += convert_int_to_bits(num=value, bits_count=9)
        for value in [self.to_port, self.to_starboard]:
            dimension_bits += convert_int_to_bits(num=value, bits_count=6)
        return dimension_bits


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
    dimension: ShipDimension
    eta: dict
    draught: float
    destination: str

    def generate_nmea(self):
        pass


class AISTrackList(BaseModel):
    tracks: List[AISTrack]


if __name__ == '__main__':

    dimension_dict = {
        'to_bow': 225,
        'to_stern': 70,

    }

    dimm = ShipDimension(**dimension_dict)
    # dimm.to_port = -1
    print(dimm.dict())