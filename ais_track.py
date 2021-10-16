from typing import List

from pydantic import BaseModel, validator

from nmea_utils import convert_int_to_bits
from ais_utils import check_mmsi_mid_code, verify_imo, verify_sixbit_ascii
from nmea_utils import add_padding
from constants import NavigationStatus, ShipType


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


class ShipEta(BaseModel):
    """
    Class represents ship's Estimated Time of Arrival in UTC.
    """
    month: int = 0
    day: int = 0
    hour: int = 24
    minute: int = 60

    class Config:
        validate_assignment = True

    @validator('month')
    def check_month_value(cls, value, field):
        if value < 0 or value > 12:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-12 range.')
        return value

    @validator('day')
    def check_day_value(cls, value, field):
        if value < 0 or value > 31:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-12 range.')
        return value

    @validator('hour')
    def check_hour_value(cls, value, field):
        if value < 0 or value > 24:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-24 range.')
        return value

    @validator('minute')
    def check_minute_value(cls, value, field):
        if value < 0 or value > 60:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-60 range.')
        return value

    @property
    def bits(self) -> str:
        eta_bits = convert_int_to_bits(num=self.month, bits_count=4)
        for value in [self.day, self.hour]:
            eta_bits += convert_int_to_bits(num=value, bits_count=5)
        eta_bits += convert_int_to_bits(num=self.minute, bits_count=6)
        return eta_bits


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
    eta: ShipEta
    draught: float
    destination: str

    class Config:
        validate_assignment = True

    @validator('mmsi')
    def check_mmsi_value(cls, value, field):
        if len(str(value)) != 9:
            raise ValueError(f'Invalid {field.name} {value}. Should consist of 9 digits')
        elif not check_mmsi_mid_code(value):
            raise ValueError(f'Invalid {field.name} {value}. Invalid MID code.')
        return value

    @validator('nav_status')
    def check_nav_status_value(cls, value, field):
        if not NavigationStatus.has_value(value):
            raise ValueError(f'Invalid {field.name} {value}.')
        return value

    @validator('lon')
    def check_lon_value(cls, value, field):
        if value < -180 or value > 180:
            raise ValueError(f'Invalid {field.name} {value}. Should be in -180 to 180 range.')
        return value

    @validator('lat')
    def check_lat_value(cls, value, field):
        if value < -90 or value > 90:
            raise ValueError(f'Invalid {field.name} {value}. Should be in -180 to 180 range.')
        return value

    @validator('speed')
    def check_speed_value(cls, value, field):
        if value < 0 or value > 102.2:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-102.2 range.')
        return value

    @validator('course')
    def check_course_value(cls, value, field):
        if value < 0 or value > 360:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-360 range.')
        return value

    @validator('imo')
    def check_imo_value(cls, value, field):
        if len(str(value)) != 7:
            raise ValueError(f'Invalid {field.name} {value}. Should consist of 7 digits')
        elif not verify_imo(imo=value):
            raise ValueError(f'Invalid {field.name} {value}. Invalid IMO checksum.')
        return value

    @validator('call_sign', 'ship_name', 'destination')
    def check_sixbit_text_value(cls, value, field):
        field_to_chars_count = {
            'call_sign': 7,
            'ship_name': 20,
            'destination': 20
        }
        required_chars_count = field_to_chars_count[field.name]
        if len(value) > required_chars_count:
            value = value[:required_chars_count]
        elif not verify_sixbit_ascii(value):
            raise ValueError(f'Invalid {field.name} {value}. Invalid sixbit ASCII chars.')
        elif len(value) < required_chars_count:
            # Add padding, if necessary
            value = add_padding(text=value, required_length=required_chars_count)
        return value

    @validator('ship_type')
    def check_ship_type_value(cls, value, field):
        if not ShipType.has_value(value):
            raise ValueError(f'Invalid {field.name} {value}.')
        return value

    @validator('draught')
    def check_draught_value(cls, value, field):
        if value < 0:
            raise ValueError(f'Invalid {field.name} {value}. Should be 0 or greater.')
        elif value > 25.5:
            value = 25.5
        return value

    def generate_nmea(self):
        pass


class AISTrackList(BaseModel):
    tracks: List[AISTrack]


if __name__ == '__main__':
    pass