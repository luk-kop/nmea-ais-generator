import pytest

from nmea_msg import NMEAMessage
from nmea_utils import convert_ais_payload_to_bits


def test_nmea_msg_multi_sentence(dummy_ais_msg_payload_type_5):
    nmea_msg = NMEAMessage(payload=dummy_ais_msg_payload_type_5)
    test_sentences = [
        '!AIVDM,2,1,1,A,533m@o`2;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*7D\r\n',
        '!AIVDM,2,2,1,A,88888888880,2*25\r\n'
    ]
    assert nmea_msg.get_sentences() == test_sentences


def test_nmea_msg_single_sentence(dummy_ais_msg_payload_type_1):
    nmea_msg = NMEAMessage(payload=dummy_ais_msg_payload_type_1)
    test_sentences = [
        '!AIVDM,1,1,,A,133m@ogP00PD;88MD5MTDww@0D7k,0*44\r\n'
    ]
    assert nmea_msg.get_sentences() == test_sentences


def test_ais_msg_payload_type_1_mmsi(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.mmsi == 205344990
    assert msg_payload._fields_to_bits()['mmsi'] == '001100001111010101000011011110'


def test_ais_msg_payload_type_1_nav_status(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.nav_status == 15
    assert msg_payload._fields_to_bits()['nav_status'] == '1111'


def test_ais_msg_payload_type_1_course(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.course == 110.7
    assert msg_payload._fields_to_bits()['course'] == '010001010011'


def test_ais_msg_payload_type_1_speed(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.speed == 0
    assert msg_payload._fields_to_bits()['speed'] == '0000000000'


def test_ais_msg_payload_type_1_lon(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.lon == 4.407046666667
    assert msg_payload._fields_to_bits()['lon'] == '0000001010000101100100000100'


def test_ais_msg_payload_type_1_lat(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.lat == 51.229636666667
    assert msg_payload._fields_to_bits()['lat'] == '001110101010000010101110110'


def test_ais_msg_payload_type_1_timestamp(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload.timestamp == 40
    assert msg_payload._fields_to_bits()['timestamp'] == '101000'


def test_ais_msg_payload_type_1_payload_bits_len(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert len(msg_payload.payload_bits) == 168


def test_ais_msg_payload_type_1_payload_bits_content(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    desired_payload = '00000100001100001111010101000011011110111110000000000000000010000001010000101100100000100001110101010' \
                      '0000101011101100100010100111111111111010000000000010100000111110011'
    assert msg_payload.payload_bits == desired_payload


def test_ais_msg_payload_type_1_payload_sixbits_list(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    assert msg_payload._payload_sixbits_list[:3] == ['000001', '000011', '000011']


def test_ais_msg_payload_type_1_speed_invalid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    with pytest.raises(Exception):
        msg_payload.speed = 'xxx'


def test_ais_msg_payload_type_1_speed_valid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    for value in ['123', '123.1', 123, 123.1]:
        msg_payload.speed = value
        assert msg_payload.speed == float(value)


def test_ais_msg_payload_type_1_course_invalid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    with pytest.raises(Exception):
        msg_payload.course = 'xxx'


def test_ais_msg_payload_type_1_course_valid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    for value in ['123', '123.1', 123, 123.1]:
        msg_payload.course = value
        assert msg_payload.course == float(value)


def test_ais_msg_payload_type_1_lon_invalid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    with pytest.raises(Exception):
        msg_payload.lon = 'xxx'


def test_ais_msg_payload_type_1_lon_valid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    for value in ['123', '123.1', 123, 123.1]:
        msg_payload.lon = value
        assert msg_payload.lon == float(value)


def test_ais_msg_payload_type_1_lat_invalid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    with pytest.raises(Exception):
        msg_payload.lat = 'xxx'


def test_ais_msg_payload_type_1_lat_valid_assignment(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    for value in ['123', '123.1', 123, 123.1]:
        msg_payload.lat = value
        assert msg_payload.lat == float(value)


def test_ais_msg_payload_type_1_constants_bits(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    desired_bits = {
        'msg_type': '000001',
        'pos_accuracy': '1',
        'raim': '0',
        'rot': '10000000',
        'radio_status': '0010100000111110011',
        'spare_type_1': '000',
        'maneuver': '00'
    }
    assert msg_payload._constants_bits == desired_bits


def test_ais_msg_payload_type_1_encode(dummy_ais_msg_payload_type_1):
    msg_payload = dummy_ais_msg_payload_type_1
    desired_output = '133m@ogP00PD;88MD5MTDww@0D7k'
    assert str(msg_payload) == desired_output


def test_ais_msg_payload_type_5_encode(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    desired_output = '533m@o`2;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880'
    assert str(msg_payload) == desired_output


def test_ais_msg_payload_type_5_before_encode(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.fill_bits == 0
    assert len(msg_payload.payload_bits) == 424


def test_ais_msg_payload_type_5_after_encode_fill_bits(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    msg_payload.encode()
    assert msg_payload.fill_bits == 2


def test_ais_msg_payload_type_5_after_encode_payload_chars_length(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    ais_payload = msg_payload.encode()
    # payload with fill-bits added
    assert len(ais_payload) == 71


def test_ais_msg_payload_type_5_after_encode_payload_bits_length(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    ais_payload = msg_payload.encode()
    # payload with fill-bits added
    payload_bits = convert_ais_payload_to_bits(payload=ais_payload)
    assert len(payload_bits) == 426


def test_ais_msg_payload_type_5_constants_bits(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    desired_bits = {
        'msg_type': '000101',
        'ais_version': '10',
        'pos_fix_type': '0001',
        'dte': '0',
        'spare_type_5': '0',
    }
    assert msg_payload._constants_bits == desired_bits


def test_ais_msg_payload_type_5_mmsi(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.mmsi == 205344990
    assert len(msg_payload._fields_to_bits()['mmsi']) == 30
    assert msg_payload._fields_to_bits()['mmsi'] == '001100001111010101000011011110'


def test_ais_msg_payload_type_5_imo(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.imo == 9134270
    assert len(msg_payload._fields_to_bits()['imo']) == 30
    assert msg_payload._fields_to_bits()['imo'] == '000000100010110110000010111110'


def test_ais_msg_payload_type_5_call_sign(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.call_sign == '3FOF8'
    assert len(msg_payload._fields_to_bits()['call_sign']) == 42
    assert msg_payload._fields_to_bits()['call_sign'] == '110011000110001111000110111000100000100000'


def test_ais_msg_payload_type_5_ship_name(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    desired_output = '0001010101100001010100101000000001000010010000010001000001010011011000001000001000001000' \
                     '00100000100000100000100000100000'
    assert msg_payload.ship_name == 'EVER DIADEM'
    assert len(msg_payload._fields_to_bits()['ship_name']) == 120
    assert msg_payload._fields_to_bits()['ship_name'] == desired_output


def test_ais_msg_payload_type_5_ship_type(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.ship_type.value == 70
    assert len(msg_payload._fields_to_bits()['ship_type']) == 8
    assert msg_payload._fields_to_bits()['ship_type'] == '01000110'


def test_ais_msg_payload_type_5_dimension(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert len(msg_payload._fields_to_bits()['dimension']) == 30
    assert msg_payload._fields_to_bits()['dimension'] == '011100001001000110000001011111'


def test_ais_msg_payload_type_5_eta(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert len(msg_payload._fields_to_bits()['eta']) == 20
    assert msg_payload._fields_to_bits()['eta'] == '01010111101110000000'


def test_ais_msg_payload_type_5_draught(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    assert msg_payload.draught == 12.2
    assert len(msg_payload._fields_to_bits()['draught']) == 8
    assert msg_payload._fields_to_bits()['draught'] == '01111010'


def test_ais_msg_payload_type_5_draught_min(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    msg_payload.draught = 0
    assert msg_payload.draught == 0
    assert len(msg_payload._fields_to_bits()['draught']) == 8
    assert msg_payload._fields_to_bits()['draught'] == '00000000'


def test_ais_msg_payload_type_5_draught_max(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    msg_payload.draught = 25.5
    assert msg_payload.draught == 25.5
    assert len(msg_payload._fields_to_bits()['draught']) == 8
    assert msg_payload._fields_to_bits()['draught'] == '11111111'


def test_ais_msg_payload_type_5_destination(dummy_ais_msg_payload_type_5):
    msg_payload = dummy_ais_msg_payload_type_5
    desired_output = '00111000010101011110000001100100111101001000101110000010000010000010000010000010000010000010' \
                     '0000100000100000100000100000'
    assert msg_payload.destination == 'NEW YORK'
    assert len(msg_payload._fields_to_bits()['destination']) == 120
    assert msg_payload._fields_to_bits()['destination'] == desired_output
