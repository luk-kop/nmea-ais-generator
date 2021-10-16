from typing import List

from pydantic import BaseModel, validator

from nmea_utils import add_padding
from ais_utils import check_mmsi_mid_code, verify_imo, verify_sixbit_ascii, ShipDimension, ShipEta
from nmea_msg import AISMsgType1, AISMsgType5
from constants import NavigationStatus, ShipType


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
    timestamp: int = 60

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

    @validator('timestamp')
    def check_timestamp_value(cls, value, field):
        if value < 0 or value > 60:
            raise ValueError(f'Invalid {field.name} {value}. Should be in 0-60 range.')
        return value

    def generate_nmea(self) -> str:
        """
        Generate NMEA msgs for AISTrack.
        """
        pass

    def generate_payload_type_1(self) -> str:
        """
        Generates payload for AIS Type 1 msg.
        """
        payload = AISMsgType1(mmsi=self.mmsi,
                              lon=self.lon,
                              lat=self.lat,
                              course=self.course,
                              nav_status=self.nav_status,
                              speed=self.speed,
                              timestamp=self.timestamp).encode()
        return payload

    def generate_payload_type_5(self) -> str:
        """
        Generates payload for AIS Type 5 msg.
        """
        payload = AISMsgType5(mmsi=self.mmsi,
                              imo=self.imo,
                              call_sign=self.call_sign,
                              ship_name=self.ship_name,
                              ship_type=self.ship_type,
                              dimension=self.dimension,
                              eta=self.eta,
                              draught=self.draught,
                              destination=self.destination).encode()
        return payload


class AISTrackList(BaseModel):
    tracks: List[AISTrack]


if __name__ == '__main__':
    pass