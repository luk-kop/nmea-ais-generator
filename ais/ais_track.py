from typing import List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, validator

from nmea.nmea_utils import add_padding
from ais.ais_utils import (
    check_mmsi_mid_code,
    verify_imo,
    verify_sixbit_ascii,
    ShipDimension,
    ShipEta,
    calculate_distance,
    calculate_new_position,
    SequentialMsgId
)
from nmea.nmea_msg import AISMsgPayloadType1, AISMsgPayloadType5, NMEAMessage
from ais.constants import NavigationStatusEnum, ShipTypeEnum, FieldCharsCountEnum


class AISTrack(BaseModel):
    """
    Class represents single AIS track.
    """
    mmsi: int
    nav_status: NavigationStatusEnum
    lon: float
    lat: float
    speed: float
    course: float
    true_heading: Optional[int] = 511
    imo: Optional[int] = 0000000
    call_sign: str
    ship_name: str
    ship_type: ShipTypeEnum
    dimension: Optional[ShipDimension] = ShipDimension()
    eta: Optional[ShipEta] = ShipEta()
    draught: float = 0
    destination: str
    timestamp: Optional[int] = 60
    _updated_at: float = datetime.utcnow().timestamp()
    _seq_msg_id: SequentialMsgId = SequentialMsgId()

    class Config:
        """
        Pydantic config class.
        """
        validate_assignment = True
        underscore_attrs_are_private = True

    @validator('mmsi')
    def check_mmsi_value(cls, value, field) -> int:
        if len(str(value)) != FieldCharsCountEnum[field.name]:
            raise ValueError(f'field value {value} is invalid. Should consist of 9 digits.')
        elif not check_mmsi_mid_code(value):
            raise ValueError(f'field value {value} is invalid. Wrong MID code.')
        return value

    @validator('lon', 'lat', 'speed', 'timestamp')
    def check_lon_lat_speed_timestamp_values(cls, value, field) -> Union[float, int]:
        valid_values = {
            'lon': {'min': -180, 'max': 180},
            'lat': {'min': -90, 'max': 90},
            'speed': {'min': 0, 'max': 102.2},
            'timestamp': {'min': 0, 'max': 60},
        }
        value_min = valid_values[field.name]['min']
        value_max = valid_values[field.name]['max']
        if value < value_min or value > value_max:
            raise ValueError(f'field value {value} is invalid. Should be in {value_min} to {value_max} range.')
        return value

    @validator('course', 'true_heading')
    def check_course_value(cls, value, field) -> float:
        if field.name == 'true_heading' and value == 511:
            # Default true_heading value
            return value
        if value < 0 or value > 360:
            raise ValueError(f'field value {value} is invalid. Should be in 0 to 360 range.')
        return value

    @validator('imo')
    def check_imo_value(cls, value, field) -> int:
        if len(str(value)) != FieldCharsCountEnum[field.name]:
            raise ValueError(f'field value {value} is invalid. Should consist of 7 digits.')
        elif not verify_imo(imo=value):
            raise ValueError(f'field value {value} is invalid. Wrong IMO checksum.')
        return value

    @validator('call_sign', 'ship_name', 'destination')
    def check_sixbit_text_value(cls, value, field) -> str:
        required_chars_count = FieldCharsCountEnum[field.name]
        if len(value) > required_chars_count:
            value = value[:required_chars_count]
        elif not verify_sixbit_ascii(value):
            raise ValueError(f'field value {value} is invalid. Wrong sixbit ASCII chars.')
        elif len(value) < required_chars_count:
            # Add padding, if necessary
            value = add_padding(text=value, required_length=required_chars_count)
        return value

    @validator('draught')
    def check_draught_value(cls, value) -> float:
        if value < 0:
            raise ValueError(f'field value {value} is invalid. Should be 0 or greater.')
        elif value > 25.5:
            value = 25.5
        return value

    def generate_nmea(self) -> List[str]:
        """
        Generate list of NMEA msgs for current AISTrack.
        """
        payloads = [self.generate_payload_type_1(), self.generate_payload_type_5()]
        msgs = []
        # sequential message ID (for multi-sentence NMEA messages)
        seq_msg_id = next(self._seq_msg_id)
        for payload in payloads:
            msgs += NMEAMessage(payload=payload).get_sentences(seq_msg_id=seq_msg_id)
        return msgs

    def generate_payload_type_1(self) -> AISMsgPayloadType1:
        """
        Generates AIS Type 1 msg object.
        """
        msg = AISMsgPayloadType1(mmsi=self.mmsi,
                                 lon=self.lon,
                                 lat=self.lat,
                                 course=self.course,
                                 true_heading=self.true_heading,
                                 nav_status=self.nav_status,
                                 speed=self.speed,
                                 timestamp=self.timestamp)
        return msg

    def generate_payload_type_5(self) -> AISMsgPayloadType5:
        """
        Generates AIS Type 5 msg object.
        """
        msg = AISMsgPayloadType5(mmsi=self.mmsi,
                                 imo=self.imo,
                                 call_sign=self.call_sign,
                                 ship_name=self.ship_name,
                                 ship_type=self.ship_type,
                                 dimension=self.dimension,
                                 eta=self.eta,
                                 draught=self.draught,
                                 destination=self.destination)
        return msg

    def update_position(self, current_timestamp: float) -> None:
        """
        Updates the AIS track position. The position will be updated every time the method is called.
        """
        # Calculate distance to new position
        distance = calculate_distance(last_timestamp=self._updated_at,
                                      current_timestamp=current_timestamp,
                                      speed=self.speed)
        # Update position update timestamp
        self._updated_at = current_timestamp
        lon_new, lat_new = calculate_new_position(lon_start=self.lon,
                                                  lat_start=self.lat,
                                                  course=self.course,
                                                  distance=distance)
        # Update AIS track coordinates
        self.lon = lon_new
        self.lat = lat_new


class AISTrackList(BaseModel):
    """
    Class represents list of AISTrack objects.
    """
    tracks: List[AISTrack]
