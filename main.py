# NMEA 0183
import textwrap


def check_sum(data: str):
    check_sum: int = 0
    for char in data:
        num = bytearray(char, encoding='utf-8')[0]
        # XOR operation.
        check_sum = (check_sum ^ num)
    # Returns only hex digits string without leading 0x.
    hex_str: str = str(hex(check_sum))[2:]
    if len(hex_str) == 2:
        return hex_str.upper()
    return f'0{hex_str}'.upper()


class AisMsgType1:
    """
    Position report
    Total 168 bits in one AIVDM msg type 1 payload
    Example: !AIVDM,1,1,,A,133m@ogP00PD;88MD5MTDww@2D7k,0*46
    """
    def __init__(self, mmsi: str,  lon: float, lat: float, course: float, nav_status: int = 15, speed: int = 0, timestamp: int = 60):

        self.msg_type = '000001'        # 6
        self.repeat_indicator = '00'    # 2
        self.mmsi = mmsi                # 30
        self.nav_status = nav_status    # 4
        self.rot = '10000000'           # 8
        self.speed = speed              # 10
        self.accuracy = '1'             # 1
        self.lon = lon                  # 28
        self.lat = lat                  # 27
        self.course = course            # 12
        self.heading = '111111111'      # 9
        self.timestamp = timestamp      # 6
        self.maneuver = '00'            # 2
        self.spare = '000'              # 3
        self.raim = '0'                 # 1
        self.radio_status = '0010100000111110011'          # 19 SOTDMA

    @property
    def mmsi(self) -> str:
        return self._mmsi

    @mmsi.setter
    def mmsi(self, mmsi) -> None:
        self._mmsi = self.num_to_bits(num=mmsi, chars_num=30)

    @property
    def nav_status(self) -> str:
        return self._nav_status

    @nav_status.setter
    def nav_status(self, nav_status) -> None:
        self._nav_status = self.num_to_bits(num=nav_status, chars_num=4)

    @property
    def lon(self) -> str:
        return self._lon

    @lon.setter
    def lon(self, lon) -> None:
        self._lon = self.num_to_bits(num=int(lon * 600000), chars_num=28)

    @property
    def lat(self) -> str:
        return self._lat

    @lat.setter
    def lat(self, lat) -> None:
        self._lat = self.num_to_bits(num=int(lat * 600000), chars_num=27)

    @property
    def course(self) -> str:
        return self._course

    @course.setter
    def course(self, course) -> None:
        # TODO: 0-3599
        self._course = self.num_to_bits(num=int(course * 10), chars_num=12)

    @property
    def speed(self) -> str:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        # TODO: 0-102.2 knots
        self._speed = self.num_to_bits(num=int(speed * 10), chars_num=10)

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp) -> None:
        # TODO: 0-60
        self._timestamp = self.num_to_bits(num=timestamp, chars_num=6)

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
        Bits payload as a list of six-character (bits) items.
        """
        return textwrap.wrap(self.payload_bits, 6)

    def encode(self):
        """
        Returns message payload in ASCII string.
        """
        payload = ''
        for item in self._payload_sixbits_list:
            decimal_num = self.bits_to_num(item)
            ascii_code = self.sixbit_decimal_to_ascii(decimal_num=decimal_num)
            payload_char = self.ascii_to_char(ascii_code=ascii_code)
            payload += payload_char
        return payload

    @staticmethod
    def num_to_bits(num: int, chars_num: int) -> str:
        """
        Converts int to bits.
        """
        return format(num, f'0{chars_num}b')

    @staticmethod
    def bits_to_num(bits: str) -> int:
        """
        Converts bits to int.
        """
        return int(bits, 2)

    @staticmethod
    def sixbit_decimal_to_ascii(decimal_num: int):
        """
        Converts six-bit decimal to ASCII code.
        """
        if decimal_num < 0 or decimal_num > 63:
            raise Exception('Wrong decimal number')
        if decimal_num not in range(33,40) and decimal_num + 8 > 40:
            decimal_num += 8
        ascii_code = decimal_num + 48
        return ascii_code

    @staticmethod
    def ascii_to_char(ascii_code: int) -> str:
        """
        Converts ASCII code to ASCII char.
        """
        return chr(ascii_code)

    def __str__(self) -> str:
        nmea_output = f'AIVDM,1,1,,A,{self.encode()},0'
        return f'!{nmea_output}*{check_sum(nmea_output)}\r\n'


class AisMsgType5:
    """
    Static and voyage related data
    Total 424 bits in one AIVDM msg type 1 payload
    Example:
    """
    def __init__(self, mmsi: str, imo: int, call_sign: str, ship_name: str, ship_type: int, eta: dict, destination: str):
        self.msg_type = '000101'  # 6
        self.repeat_indicator = '00'  # 2
        self.mmsi = mmsi  # 30
        self.ais_version = '10'
        self.imo = imo
        self.call_sign = call_sign
        self.ship_name = ship_name
        self.ship_type = ship_type  # 1-99
        # dimension
        self.to_bow = ''
        self.to_stern = ''
        self.to_stern = ''
        self.to_port = ''
        self.pos_fix_type = '0001'  # GPS
        self.eta = eta
        # self.eta_month = ''         # 1-12
        # self.eta_day = ''           # 1-31
        # self.eta_hour = ''          # 0-23
        # self.eta_minute = ''        # 0-59
        self.draught = ''
        self.destination = destination
        self.dte = '0'
        self.spare = '0'


if __name__ == '__main__':
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, timestamp=40)
    print(msg)


