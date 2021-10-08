import pytest

from main import AisMsgType1


def test_aismsg_mmsi():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, nav_status=15)
    assert msg.mmsi == '001100001111010101000011011110'


def test_aismsg_nav_status():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, nav_status=15)
    assert msg.nav_status == '1111'


def test_aismsg_course():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7)
    assert msg.course == '010001010011'


def test_aismsg_speed():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7)
    assert msg.speed == '0000000000'


def test_aismsg_lon():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7)
    assert msg.lon == '0000001010000101100100000100'


def test_aismsg_lat():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7)
    assert msg.lat == '001110101010000010101110110'


def test_aismsg_timestamp():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, timestamp=40)
    assert msg.timestamp == '101000'


def test_aismsg_payload_bits_len():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, timestamp=40)
    assert len(msg.payload_bits) == 168


def test_aismsg_payload_bits_content():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, timestamp=40)
    payload = '00000100001100001111010101000011011110111110000000000000000010000001010000101100100000100001110101010' \
              '0000101011101100100010100111111111111010000000000010100000111110011'
    assert msg.payload_bits == payload


def test_aismsg_payload_sixbits_list():
    msg = AisMsgType1(mmsi=205344990, speed=0, lon=4.407046666667, lat=51.229636666667, course=110.7, timestamp=40)
    assert msg._payload_sixbits_list[:3] == ['000001', '000011', '000011']


def test_aismsg_bits_to_num():
    test_dir = {
        '0001': 1,
        '0010': 2,
        '101000': 40,
        '011011': 27,
        '110011': 51
    }
    for bits, int_num in test_dir.items():
        assert AisMsgType1.bits_to_num(bits=bits) == int_num


def test_aismsg_sixbit_decimal_to_ascii_correct():
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=0) == 48
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=13) == 61
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=33) == 89
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=40) == 96
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=41) == 97
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=45) == 101
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=59) == 115
    assert AisMsgType1.sixbit_decimal_to_ascii(decimal_num=63) == 119


def test_aismsg_sixbit_decimal_to_ascii_incorrect():
    with pytest.raises(Exception):
        AisMsgType1.sixbit_decimal_to_ascii(decimal_num=-1)
    with pytest.raises(Exception):
        AisMsgType1.sixbit_decimal_to_ascii(decimal_num=64)

