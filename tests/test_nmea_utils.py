import pytest

from nmea.nmea_utils import (
    get_ascii_code_of_char,
    get_char_of_ascii_code,
    convert_int_to_bits,
    convert_bits_to_int,
    convert_ascii_code_to_decimal,
    convert_decimal_to_ascii_code,
    convert_ascii_char_to_ascii6_code,
    add_padding,
    add_padding_0_bits,
    convert_ais_payload_to_bits,
    nmea_checksum
)


def test_get_ascii_code_of_char():
    assert get_ascii_code_of_char(char='A') == 65
    assert get_ascii_code_of_char(char='A') == 65
    assert get_ascii_code_of_char(char='?') == 63
    assert get_ascii_code_of_char(char='_') == 95
    assert get_ascii_code_of_char(char='_') != 96


def test_get_char_of_ascii_code():
    assert get_char_of_ascii_code(ascii_code=65) == 'A'
    assert get_char_of_ascii_code(ascii_code=64) == '@'
    assert get_char_of_ascii_code(ascii_code=48) == '0'
    assert get_char_of_ascii_code(ascii_code=119) == 'w'
    assert get_char_of_ascii_code(ascii_code=119) != 'x'


def test_convert_int_to_bits_unsigned_int():
    int_to_bits = {
        1: {
            'bits_count': 4,
            'bits_str': '0001'
        },
        2: {
            'bits_count': 2,
            'bits_str': '10'
        },
        40: {
            'bits_count': 6,
            'bits_str': '101000'
        },
        27: {
            'bits_count': 6,
            'bits_str': '011011'
        },
        51: {
            'bits_count': 7,
            'bits_str': '0110011'
        },
    }
    for int_num, bits in int_to_bits.items():
        assert convert_int_to_bits(num=int_num, bits_count=bits['bits_count']) == bits['bits_str']
    assert convert_int_to_bits(num=15) == '001111'


def test_convert_int_to_bits_signed_int():
    int_to_bits = {
        2644228: {
            'bits_count': 28,
            'bits_str': '0000001010000101100100000100'
        },
        -2644228: {
            'bits_count': 28,
            'bits_str': '1111110101111010011011111100'
        },
        -123456: {
            'bits_count': 24,
            'bits_str': '111111100001110111000000'
        },
        27: {
            'bits_count': 6,
            'bits_str': '011011'
        },
        -51: {
            'bits_count': 8,
            'bits_str': '11001101'
        },
    }
    for int_num, bits in int_to_bits.items():
        assert convert_int_to_bits(num=int_num, bits_count=bits['bits_count'], signed=True) == bits['bits_str']
    assert convert_int_to_bits(num=15) == '001111'


def test_convert_bits_to_int():
    bits_to_int = {
        '0001': 1,
        '0010': 2,
        '101000': 40,
        '011011': 27,
        '110011': 51
    }
    for bits, int_num in bits_to_int.items():
        assert convert_bits_to_int(bits=bits) == int_num


def test_convert_decimal_to_ascii_code():
    decimal_to_ascii = {
        0: 48,
        13: 61,
        24: 72,
        32: 80,
        33: 81,
        36: 84,
        39: 87,
        40: 96,
        41: 97,
        45: 101,
        55: 111,
        59: 115,
        63: 119,
    }
    for decimal, ascii in decimal_to_ascii.items():
        assert convert_decimal_to_ascii_code(decimal_num=decimal) == ascii


def test_convert_decimal_to_ascii_code_incorrect():
    with pytest.raises(Exception):
        convert_decimal_to_ascii_code(decimal_num=-1)
    with pytest.raises(Exception):
        convert_decimal_to_ascii_code(decimal_num=64)


def test_convert_ascii_code_to_decimal():
    decimal_to_ascii = {
        0: 48,
        13: 61,
        24: 72,
        32: 80,
        33: 81,
        36: 84,
        39: 87,
        40: 96,
        41: 97,
        45: 101,
        55: 111,
        59: 115,
        63: 119,
    }
    for decimal, ascii in decimal_to_ascii.items():
        assert convert_ascii_code_to_decimal(ascii_code=ascii) == decimal


def test_convert_ascii_code_to_decimal_incorrect():
    with pytest.raises(Exception):
        convert_ascii_code_to_decimal(ascii_code=47)
    with pytest.raises(Exception):
        convert_ascii_code_to_decimal(ascii_code=88)
    with pytest.raises(Exception):
        convert_ascii_code_to_decimal(ascii_code=95)
    with pytest.raises(Exception):
        convert_ascii_code_to_decimal(ascii_code=120)

def test_convert_ascii_char_to_ascii6_code():
    ascii_to_ascii6 = {
        '@': 0,
        'A': 1,
        'M': 13,
        'O': 15,
        'Z': 26,
        '[': 27,
        ' ': 32,
        '&': 38,
        '0': 48,
        '9': 57,
        ':': 58,
        '=': 61
    }
    for ascii, ascii6 in ascii_to_ascii6.items():
        assert convert_ascii_char_to_ascii6_code(char=ascii) == ascii6


def test_add_padding():
    assert add_padding(text='text', required_length=5) == 'text '
    assert add_padding(text='text', required_length=6, padding_char='#') == 'text##'
    assert add_padding(text='text', required_length=4, padding_char='#') == 'text'
    assert add_padding(text='text', required_length=4) == 'text'


def test_add_padding_incorrect():
    with pytest.raises(Exception):
        add_padding(text='text', required_length=3)


def test_add_padding_0_bits():
    assert add_padding_0_bits(bits_string='001100', required_length=8) == ('00110000', 2)


def test_convert_ais_payload_to_bits():
    ais_payload = '55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880'
    ais_payload_bits = '0001010001010011110111011010101001100000000000100010110110000010111110110011000110001111000' \
                       '11011100010000010000000010101011000010101001010000000010000100100000100010000010100110110000' \
                       '010000010000010000010000010000010000010000010000001000110011100001001000110000001011111000101' \
                       '010111101110000000011110100011100001010101111000000110010011110100100010111000001000001000001' \
                       '000001000001000001000001000001000001000001000001000000000'
    assert convert_ais_payload_to_bits(payload=ais_payload) == ais_payload_bits


def test_nmea_checksum_correct():
    checksum = nmea_checksum('AIVDM,2,1,8,A,56;OaD02B8EL990b221`P4v1T4pN0HDpN2222216HHN>B6U30A2hCDhD`888,0')
    assert checksum == '4D'
    checksum = nmea_checksum('AIVDM,2,2,8,A,88888888880,2')
    assert checksum == '2C'


def test_nmea_checksum_incorrect():
    checksum = nmea_checksum('AIVDM,2,1,8,A,56;OaD02B8EL990b221`P4v1T4pN0HDpN2222216HHN>B6U30A2hCDhD`888,0')
    assert checksum != 'XX'
    checksum = nmea_checksum('XXXXX')
    assert checksum != '2C'
