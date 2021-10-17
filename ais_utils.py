from pydantic import BaseModel, validator, root_validator

from constants import MmsiCountryEnum
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

    @root_validator(pre=True)
    def check_attrs_omitted(cls, values):
        """
        Set all attributes to 0 if any of the attributes are not passed in.
        """
        attrs = ['to_bow', 'to_stern', 'to_port', 'to_starboard']
        for attr in attrs:
            if attr not in values:
                values = {k: 0 for k, v in values.items()}
                return values
        return values

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


def get_first_3_digits(value: int) -> int:
    """
    Returns first 3 digits of given int.
    """
    return int(str(value)[:3])


def check_mmsi_mid_code(mmsi: int) -> bool:
    """
    Checks whether MMSI number contain valid MID.
    """
    country_code = get_first_3_digits(mmsi)
    return MmsiCountryEnum.has_value(country_code)


def verify_imo(imo: int) -> bool:
    """
    Checks that provided number is valid IMO number.
    Source: http://tarkistusmerkit.teppovuori.fi/coden.htm
    """
    checksum_calculated, checksum = 0, ''
    for pos, digit in enumerate(str(imo)[::-1], 1):
        if pos == 1:
            checksum = digit
        else:
            checksum_calculated += int(pos) * int(digit)
    return str(checksum_calculated)[-1] == checksum


def verify_sixbit_ascii(text: str) -> bool:
    """
    Checks that all chars in given text are valid sixbit ASCII chars.
    """
    sixbit_ascii = r'@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_ !"#$%&\()*+,-./0123456789:;<=>?'
    for char in text:
        if char not in sixbit_ascii:
            return False
    return True


