from abc import ABC, abstractmethod
import textwrap
from typing import Union, List, Dict

from pydantic import BaseModel

from nmea.nmea_utils import convert_bits_to_int, convert_int_to_bits, get_char_of_ascii_code, convert_decimal_to_ascii_code, \
    convert_ascii_char_to_ascii6_code, add_padding, add_padding_0_bits, nmea_checksum
from ais.ais_utils import ShipDimension, ShipEta
from ais.constants import FieldBitsCountEnum, AISMsgType1ConstsEnum, NavigationStatusEnum, ShipTypeEnum, \
    AISMsgType5ConstsEnum, FieldCharsCountEnum


class AISMsgPayload(BaseModel, ABC):
    """
    Class represent an abstract class which acts as a parent class for other AIS msgs.
    """
    repeat_indicator: int = 0
    mmsi: int
    # Number of fill bits requires to pad the data payload to a 6 bit boundary (range 0-5).
    fill_bits: int = 0

    @abstractmethod
    def payload_bits(self) -> None:
        pass

    @property
    def _payload_sixbits_list(self) -> List[str]:
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

    def __str__(self) -> str:
        return f'{self.encode()}'

    class Config:
        """
        Pydantic config class.
        """
        validate_assignment = True
        underscore_attrs_are_private = True


class AISMsgPayloadType1(AISMsgPayload):
    """
    Class represents payload of AIS msg type 1 (Position Report Class A).
    Total number of bits in one AIS msg type 1 payload - 168 bits.
    Payload example: 133m@ogP00PD;88MD5MTDww@2D7k
    """
    nav_status: NavigationStatusEnum
    speed: float = 0
    lon: float
    lat: float
    course: float
    # True heading - default value, not available (511)
    true_heading: int = 511
    timestamp: int = 60

    @property
    def _constants_bits(self) -> Dict[str, str]:
        """
        Returns AIS const fields in bits.
        """
        bits, const = FieldBitsCountEnum, AISMsgType1ConstsEnum.dict()
        return {name: convert_int_to_bits(num=value, bits_count=bits[name]) for name, value in const.items()}

    @property
    def payload_bits(self) -> str:
        """
        Returns msg payload as a bit string.
        """
        # Constants in bits
        consts = self._constants_bits
        # Object attrs (fields) in bits
        fields = self._fields_to_bits()
        payload_fields_list = [
            consts['msg_type'],
            fields['repeat_indicator'],
            fields['mmsi'],
            fields['nav_status'],
            consts['rot'],
            fields['speed'],
            consts['pos_accuracy'],
            fields['lon'],
            fields['lat'],
            fields['course'],
            fields['true_heading'],
            fields['timestamp'],
            consts['maneuver'],
            consts['spare_type_1'],
            consts['raim'],
            consts['radio_status']
        ]
        return ''.join(payload_fields_list)

    def _fields_to_bits(self) -> Dict[str, str]:
        """
        Converts AIS fields (attrs) values to bits.
        """
        fields: dict = self.dict(exclude={'fill_bits'})
        fields_in_bits = {}

        for field, value in fields.items():
            bits_count = FieldBitsCountEnum[field]
            if field in ['lon', 'lat']:
                # Conversion for 'lat' & 'lon' fields.
                value = int(value * 600000)
                bits_value = convert_int_to_bits(num=value, bits_count=bits_count, signed=True)
            else:
                if field in ['course', 'speed']:
                    # Change value for 'course' & 'speed' fields.
                    value = int(value * 10)
                bits_value = convert_int_to_bits(num=value, bits_count=bits_count)
            fields_in_bits[field] = bits_value
        return fields_in_bits


class AISMsgPayloadType5(AISMsgPayload):
    """
    Class represents payload of AIS msg type 5 (Static and Voyage Related Data).
    Total number of bits in one AIS msg type 5 payload - 424 bits (without fill_bits).
    The msg payload will be split into two AIVDM messages due to the maximum NMEA frame size limitation (82 chars).
    Payload example: 55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880
    """
    imo: int
    call_sign: str
    ship_name: str
    ship_type: ShipTypeEnum
    dimension: ShipDimension
    eta: ShipEta
    draught: float
    destination: str

    @property
    def _constants_bits(self) -> Dict[str, str]:
        """
        Returns AIS const fields in bits.
        """
        bits, const = FieldBitsCountEnum, AISMsgType5ConstsEnum.dict()
        return {name: convert_int_to_bits(num=value, bits_count=bits[name]) for name, value in const.items()}

    @property
    def payload_bits(self) -> str:
        """
        Returns msg payload as a bit string.
        """
        # Constants in bits
        consts = self._constants_bits
        # Object attrs (fields) in bits
        fields = self._fields_to_bits()
        payload_fields_list = [
            consts['msg_type'],
            fields['repeat_indicator'],
            fields['mmsi'],
            consts['ais_version'],
            fields['imo'],
            fields['call_sign'],
            fields['ship_name'],
            fields['ship_type'],
            fields['dimension'],
            consts['pos_fix_type'],
            fields['eta'],
            fields['draught'],
            fields['destination'],
            consts['dte'],
            consts['spare_type_5']
        ]
        return ''.join(payload_fields_list)

    def _fields_to_bits(self) -> Dict[str, str]:
        """
        Converts AIS fields (attrs) values to bits.
        """
        fields: dict = self.dict(exclude={'fill_bits', 'dimension', 'eta'})
        fields_in_bits = {}

        for field, value in fields.items():
            bits_count = FieldBitsCountEnum[field]
            if field in ['call_sign', 'ship_name', 'destination']:
                # Add padding - only for testing purposes because the data validation is done in the AISTrack class.
                chars_count = FieldCharsCountEnum[field]
                if len(value) != chars_count:
                    value = add_padding(text=value, required_length=chars_count)
                bits_value = ''
                for char in value:
                    # Get ASCII6 code from ASCII char.
                    ascii6_code: int = convert_ascii_char_to_ascii6_code(char=char)
                    # Convert ASCII6 code to bits.
                    six_bits: str = convert_int_to_bits(num=ascii6_code, bits_count=6)
                    bits_value += six_bits
                if field == 'call_sign' and len(bits_value) < bits_count:
                    # Only for 'call_sign'
                    bits_value, self.fill_bits = add_padding_0_bits(bits_string=bits_value, required_length=bits_count)
            else:
                if field == 'draught':
                    value = int(value * 10)
                bits_value = convert_int_to_bits(num=value, bits_count=bits_count)
            fields_in_bits[field] = bits_value
        # Add 'dimension' & 'eta' fields
        fields_in_bits['dimension'] = self.dimension.bits
        fields_in_bits['eta'] = self.eta.bits
        return fields_in_bits


class NMEAMessage:
    """
    Class represents NMEA message. It can consist of a single sequence or multiple sequences.
    """
    def __init__(self, payload: Union[AISMsgPayloadType1, AISMsgPayloadType5]) -> None:
        self.nmea_msg_type = 'AIVDM'
        self.payload = payload
        self.payload_parts: list = textwrap.wrap(payload.encode(), 60)
        # Default 1 unless it is multi-sentence msg
        self.number_of_sentences = len(self.payload_parts)
        self.ais_channel = 'A'

    def get_sentences(self, seq_msg_id: int = 0) -> List[str]:
        """
        Return list of NMEA sentences.
        """
        nmea_sentences = []
        for sentence_number, sentence_payload in enumerate(self.payload_parts, 1):
            # Number of unused bits at end of encoded data (0-5)
            fill_bits = self.payload.fill_bits if sentence_number == self.number_of_sentences else 0
            # Can be digit between 0-9, but is common for both messages.
            sequential_msg_id = seq_msg_id if self.number_of_sentences > 1 else ''
            # Data from which the checksum will be calculated.
            sentence_data = f'{self.nmea_msg_type},{self.number_of_sentences},{sentence_number},{sequential_msg_id},' \
                            f'{self.ais_channel},{sentence_payload},{fill_bits}'
            nmea_sentences.append(f'!{sentence_data}*{nmea_checksum(sentence_data)}\r\n')
        return nmea_sentences


if __name__ == '__main__':
    pass
