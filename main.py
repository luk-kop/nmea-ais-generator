import textwrap

from utils import convert_bits_to_int, convert_int_to_bits, get_char_of_ascii_code, convert_decimal_to_ascii_code, \
    convert_ascii_char_to_ascii6_code, get_ascii_code_of_char, add_padding, add_padding_0_bits, nmea_check_sum


class AisMsgType1:
    """
    Class represents payload of AIS msg type 1 (Position Report Class A).
    Total number of bits in one AIS msg type 1 payload - 168 bits.
    Payload example: 133m@ogP00PD;88MD5MTDww@2D7k
    """
    def __init__(self, mmsi: int,  lon: float, lat: float, course: float, nav_status: int = 15, speed: int = 0, timestamp: int = 60) -> None:
        self.msg_type = convert_int_to_bits(num=1, bits_count=6)
        self.repeat_indicator = convert_int_to_bits(num=0, bits_count=2)
        self.mmsi = mmsi
        self.nav_status = nav_status
        # ROT - default value, no turn info available (128)
        self.rot = convert_int_to_bits(num=128, bits_count=8)
        self.speed = speed
        # Position accuracy - high (1)
        self.accuracy = convert_int_to_bits(num=1, bits_count=1)
        self.lon = lon
        self.lat = lat
        self.course = course
        # True heading - default value, not available (511)
        self.heading = convert_int_to_bits(num=511, bits_count=9)
        self.timestamp = timestamp      # 6
        self.maneuver = convert_int_to_bits(num=0, bits_count=2)
        self.spare = convert_int_to_bits(num=0, bits_count=3)
        # RAIM - not in use (0)
        self.raim = convert_int_to_bits(num=0, bits_count=1)
        # Dummy SOTDMA data
        self.radio_status = '0010100000111110011'

    @property
    def mmsi(self) -> str:
        return self._mmsi

    @mmsi.setter
    def mmsi(self, mmsi) -> None:
        self._mmsi = convert_int_to_bits(num=mmsi, bits_count=30)

    @property
    def nav_status(self) -> str:
        return self._nav_status

    @nav_status.setter
    def nav_status(self, nav_status) -> None:
        self._nav_status = convert_int_to_bits(num=nav_status, bits_count=4)

    @property
    def lon(self) -> str:
        return self._lon

    @lon.setter
    def lon(self, lon) -> None:
        self._lon = convert_int_to_bits(num=int(lon * 600000), bits_count=28)

    @property
    def lat(self) -> str:
        return self._lat

    @lat.setter
    def lat(self, lat) -> None:
        self._lat = convert_int_to_bits(num=int(lat * 600000), bits_count=27)

    @property
    def course(self) -> str:
        return self._course

    @course.setter
    def course(self, course) -> None:
        if course < 0 or course > 360:
            raise ValueError(f'Invalid course {course}. Should be in 0-360 range.')
        self._course = convert_int_to_bits(num=int(course * 10), bits_count=12)

    @property
    def speed(self) -> str:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        if speed < 0 or speed > 102.2:
            raise ValueError(f'Invalid speed {speed}. Should be in 0-102.2 range.')
        self._speed = convert_int_to_bits(num=int(speed * 10), bits_count=10)

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp) -> None:
        if timestamp not in range(0, 61):
            raise ValueError(f'Invalid timestamp {timestamp}. Should be in 0-60 range.')
        self._timestamp = convert_int_to_bits(num=timestamp, bits_count=6)

    @property
    def payload_bits(self) -> str:
        """
        Returns msg payload as a bit string.
        """
        return f'{self.msg_type}{self.repeat_indicator}{self.mmsi}{self.nav_status}{self.rot}{self.speed}' \
            f'{self.accuracy}{self.lon}{self.lat}{self.course}{self.heading}{self.timestamp}{self.maneuver}' \
            f'{self.spare}{self.raim}{self.radio_status}'

    @property
    def _payload_sixbits_list(self) -> list:
        """
        Returns msg payload as a list of six-character (bits) items.
        """
        return textwrap.wrap(self.payload_bits, 6)

    def encode(self) -> str:
        """
        Returns message payload as a string of ASCII chars (AIVDM Payload Armoring)
        """
        payload = ''
        for item in self._payload_sixbits_list:
            decimal_num = convert_bits_to_int(bits=item)
            ascii_code = convert_decimal_to_ascii_code(decimal_num=decimal_num)
            payload_char = get_char_of_ascii_code(ascii_code=ascii_code)
            payload += payload_char
        return payload

    def __str__(self) -> str:
        nmea_output = f'AIVDM,1,1,,A,{self.encode()},0'
        return f'!{nmea_output}*{nmea_check_sum(nmea_output)}\r\n'


class AisMsgType5:
    """
    Class represents payload of AIS msg type 5 (Static and Voyage Related Data).
    Total number of bits in one AIS msg type 5 payload - 424 bits.
    The msg payload will be split into two AIVDM messages due to the maximum NMEA frame size limitation (82 chars).
    Payload example: 55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880
    """
    def __init__(self, mmsi: int, imo: int, call_sign: str, ship_name: str, ship_type: int, dimension: dict, eta: dict, draught: float, destination: str):
        self.msg_type = convert_int_to_bits(num=5, bits_count=6)
        self.repeat_indicator = convert_int_to_bits(num=0, bits_count=2)
        self.mmsi = mmsi
        # AIS version - station compliant with ITU-R M.1371-5 (2)
        self.ais_version = convert_int_to_bits(num=2, bits_count=2)
        self.imo = imo
        self.call_sign = call_sign
        self.ship_name = ship_name
        self.ship_type = ship_type
        self.dimension = dimension
        # Type of position fixing device - GPS (1)
        self.pos_fix_type = convert_int_to_bits(num=1, bits_count=4)
        self.eta = eta
        self.draught = draught
        self.destination = destination
        # DTE - ready (0)
        self.dte = convert_int_to_bits(num=0, bits_count=1)
        self.spare = convert_int_to_bits(num=0, bits_count=1)
        # Number of fill bits requires to pad the data payload to a 6 bit boundary (range 0-5).
        self.fill_bits = 0

    @property
    def mmsi(self) -> str:
        return self._mmsi

    @mmsi.setter
    def mmsi(self, value) -> None:
        self._mmsi = convert_int_to_bits(num=value, bits_count=30)

    @property
    def imo(self) -> str:
        return self._imo

    @imo.setter
    def imo(self, value) -> None:
        self._imo = convert_int_to_bits(num=value, bits_count=30)

    @property
    def call_sign(self) -> str:
        return self._call_sign

    @call_sign.setter
    def call_sign(self, call_sign) -> None:
        # TODO: enum for counts
        required_bit_count = 42
        required_char_count = 7
        if len(call_sign) not in range(0, required_char_count + 1):
            raise ValueError(f'Invalid call_sign {call_sign} (max {required_char_count} chars).')
        if len(call_sign) == 0:
            call_sign = '@' * required_char_count
        else:
            # call_sign with padding, if necessary
            call_sign = add_padding(text=call_sign, required_length=required_char_count)
        call_sign_bits = ''
        for char in call_sign:
            # Get ASCII6 code from ASCII char.
            ascii6_code: int = convert_ascii_char_to_ascii6_code(char=char)
            # Convert ASCII6 code to bits.
            six_bits: str = convert_int_to_bits(num=ascii6_code, bits_count=6)
            call_sign_bits += six_bits
        if len(call_sign_bits) < required_bit_count:
            call_sign_bits, self.fill_bits = add_padding_0_bits(bits_string=call_sign_bits, required_length=required_bit_count)
        self._call_sign = call_sign_bits

    @property
    def ship_name(self) -> str:
        return self._ship_name

    @ship_name.setter
    def ship_name(self, ship_name) -> None:
        # TODO: enum for counts
        required_bit_count = 120
        required_char_count = 20
        if len(ship_name) not in range(0, required_char_count + 1):
            raise ValueError(f'Invalid ship_name {ship_name} (max {required_char_count} chars).')
        if len(ship_name) == 0:
            ship_name = '@' * required_char_count
        else:
            # call_sign with padding, if necessary
            ship_name = add_padding(text=ship_name, required_length=required_char_count)
        ship_name_bits = ''
        for char in ship_name:
            # Get ASCII6 code from ASCII char.
            ascii6_code: int = convert_ascii_char_to_ascii6_code(char=char)
            # Convert ASCII6 code to bits.
            six_bits: str = convert_int_to_bits(num=ascii6_code, bits_count=6)
            ship_name_bits += six_bits
        # if len(ship_name_bits) < required_bit_count:
        #     ship_name_bits, self.fill_bits = add_padding_0_bits(bits_string=ship_name_bits, required_length=required_bit_count)
        self._ship_name = ship_name_bits

    @property
    def ship_type(self) -> str:
        return self._ship_type

    @ship_type.setter
    def ship_type(self, value) -> None:
        if value not in range(1, 100):
            raise ValueError(f'Invalid ship_type {value}. Should be in 1-99 range.')
        self._ship_type = convert_int_to_bits(num=value, bits_count=8)

    @property
    def dimension(self) -> str:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension) -> None:
        self._dimension = ShipDimension(dimension_data=dimension).bits

    @property
    def eta(self) -> str:
        return self._eta

    @eta.setter
    def eta(self, eta) -> None:
        self._eta = ShipEta(eta_data=eta).bits

    @property
    def draught(self) -> str:
        return self._draught

    @draught.setter
    def draught(self, value) -> None:
        if value < 0:
            raise ValueError(f'Invalid draught {value}. Should be 0 or greater.')
        elif value > 25.5:
            value = 25.5
        self._draught = convert_int_to_bits(num=int(value * 10), bits_count=8)

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, destination) -> None:
        # TODO: enum for counts
        required_bit_count = 120
        required_char_count = 20
        if len(destination) not in range(0, required_char_count + 1):
            raise ValueError(f'Invalid destination {destination} (max {required_char_count} chars).')
        if len(destination) == 0:
            destination = '@' * required_char_count
        else:
            # call_sign with padding, if necessary
            destination = add_padding(text=destination, required_length=required_char_count)
        destination_bits = ''
        for char in destination:
            # Get ASCII6 code from ASCII char.
            ascii6_code: int = convert_ascii_char_to_ascii6_code(char=char)
            # Convert ASCII6 code to bits.
            six_bits: str = convert_int_to_bits(num=ascii6_code, bits_count=6)
            destination_bits += six_bits
        # if len(destination_bits) < required_bit_count:
        #     destination_bits, self.fill_bits = add_padding_0_bits(bits_string=destination_bits,
        #                                                         required_length=required_bit_count)
        self._destination = destination_bits

    @property
    def payload_bits(self) -> str:
        """
        Returns msg payload as a bit string.
        Payload without fill-bits (padding) added to last six-bit item (nibble).
        """
        return f'{self.msg_type}{self.repeat_indicator}{self.mmsi}{self.ais_version}{self.imo}{self.call_sign}' \
               f'{self.ship_name}{self.ship_type}{self.dimension}{self.pos_fix_type}{self.eta}{self.draught}' \
               f'{self.destination}{self.dte}{self.spare}'

    @property
    def _payload_sixbits_list(self) -> list:
        """
        Returns msg payload as a list of six-character (bits) items.
        """
        return textwrap.wrap(self.payload_bits, 6)

    def encode(self) -> str:
        """
        Returns message payload as a string of ASCII chars (AIVDM Payload Armoring).
        Adds fill-bits (padding) to last six-bit item, if necessary.
        """
        payload = ''
        for item in self._payload_sixbits_list:
            # Add fill-bits (padding) to last six-bit item, if necessary
            while len(item) < 6:
                item += '0'
                self.fill_bits += 1
            decimal_num = convert_bits_to_int(bits=item)
            ascii_code = convert_decimal_to_ascii_code(decimal_num=decimal_num)
            payload_char = get_char_of_ascii_code(ascii_code=ascii_code)
            payload += payload_char
        return payload


class ShipDimension:
    """
    Class represents the dimension of the ship.
    All dimensions in meters.
    """
    def __init__(self, dimension_data: dict) -> None:
        self.to_bow = dimension_data.get('to_bow', 0)
        self.to_stern = dimension_data.get('to_stern', 0)
        self.to_port = dimension_data.get('to_port', 0)
        self.to_starboard = dimension_data.get('to_starboard', 0)

    @property
    def to_bow(self) -> int:
        return self._to_bow

    @to_bow.setter
    def to_bow(self, value) -> None:
        if value < 0:
            raise ValueError(f'Invalid to_bow {value}. Should be 0 or greater.')
        elif value > 511:
            value = 511
        self._to_bow = value

    @property
    def to_stern(self) -> int:
        return self._to_stern

    @to_stern.setter
    def to_stern(self, value) -> None:
        if value < 0:
            raise ValueError(f'Invalid to_stern {value}. Should be 0 or greater.')
        elif value > 511:
            value = 511
        self._to_stern = value

    @property
    def to_port(self) -> int:
        return self._to_port

    @to_port.setter
    def to_port(self, value) -> None:
        if value < 0:
            raise ValueError(f'Invalid to_port {value}. Should be 0 or greater.')
        elif value > 63:
            value = 63
        self._to_port = value

    @property
    def to_starboard(self) -> int:
        return self._to_starboard

    @to_starboard.setter
    def to_starboard(self, value) -> None:
        if value < 0:
            raise ValueError(f'Invalid to_starboard {value}. Should be 0 or greater.')
        elif value > 63:
            value = 63
        self._to_starboard = value

    @property
    def bits(self) -> str:
        dimension_bits = ''
        for value in [self.to_bow, self.to_stern]:
            dimension_bits += convert_int_to_bits(num=value, bits_count=9)
        for value in [self.to_port, self.to_starboard]:
            dimension_bits += convert_int_to_bits(num=value, bits_count=6)
        return dimension_bits


class ShipEta:
    """
    Class represents ship's Estimated Time of Arrival in UTC.
    """
    def __init__(self, eta_data: dict) -> None:
        self.month = eta_data.get('month', 0)
        self.day = eta_data.get('day', 0)
        self.hour = eta_data.get('hour', 24)
        self.minute = eta_data.get('minute', 60)

    @property
    def month(self) -> int:
        return self._month

    @month.setter
    def month(self, value) -> None:
        if value < 0 or value > 12:
            raise ValueError(f'Invalid month {value}. Should be in 0-12 range.')
        self._month = value

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, value) -> None:
        if value < 0 or value > 31:
            raise ValueError(f'Invalid day {value}. Should be in 0-12 range.')
        self._day = value

    @property
    def hour(self) -> int:
        return self._hour

    @hour.setter
    def hour(self, value) -> None:
        if value < 0 or value > 24:
            raise ValueError(f'Invalid hour {value}. Should be in 0-24 range.')
        self._hour = value

    @property
    def minute(self) -> int:
        return self._minute

    @minute.setter
    def minute(self, value) -> None:
        if value < 0 or value > 60:
            raise ValueError(f'Invalid minute {value}. Should be in 0-60 range.')
        self._minute = value

    @property
    def bits(self) -> str:
        eta_bits = convert_int_to_bits(num=self.month, bits_count=4)
        for value in [self.day, self.hour]:
            eta_bits += convert_int_to_bits(num=value, bits_count=5)
        eta_bits += convert_int_to_bits(num=self.minute, bits_count=6)
        return eta_bits


if __name__ == '__main__':
    # Only for tests
    dimension_dict = {
        'to_bow': 225,
        'to_stern': 70,
        'to_port': 1,
        'to_starboard': 31
    }
    eta_dict = {
        'month': 5,
        'day': 15,
        'hour': 14,
        'minute': 0
    }
    msg = AisMsgType5(mmsi=205344990,
                      imo=9134270,
                      call_sign='3FOF8',
                      ship_name='EVER DIADEM',
                      ship_type=70,
                      dimension=dimension_dict,
                      eta=eta_dict,
                      draught=12.2,
                      destination='NEW YORK')
    print(msg.encode())



