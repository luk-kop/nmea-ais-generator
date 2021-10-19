import pytest

from nmea_msg import NMEAMessage


def test_nmea_msg_multi_sentence(dummy_ais_msg_type_5):
    nmea_msg = NMEAMessage(payload=dummy_ais_msg_type_5)
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
