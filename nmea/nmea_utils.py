def get_ascii_code_of_char(char: str) -> int:
    """
    Returns ACSII code (decimal) of provided char.
    """
    return bytearray(char, encoding='utf-8')[0]


def get_char_of_ascii_code(ascii_code: int) -> str:
    """
    Returns char for provided ASCII code (decimal).
    """
    return chr(ascii_code)


def convert_int_to_bits(num: int, bits_count: int = 6, signed: bool = False) -> str:
    """
    Converts int to bits string.
    """
    if signed:
        if num < 0:
            return format(num & (pow(2, bits_count) - 1), f'0{bits_count}b')
    return format(num, f'0{bits_count}b')


def convert_bits_to_int(bits: str) -> int:
    """
    Converts bits string to int.
    """
    return int(bits, 2)


def convert_ascii_char_to_ascii6_code(char: str) -> int:
    """
    Convert ASCII char to ASCII6 code.
    """
    ascii_code = ord(char)
    if 64 <= ascii_code <= 95:
        ascii6_code = ascii_code - 64
    elif 32 <= ascii_code <= 63:
        ascii6_code = ascii_code
    else:
        raise ValueError(f'Invalid character {ascii_code}')
    return ascii6_code


def convert_ascii_code_to_decimal(ascii_code: int) -> int:
    """
    Converts ASCII code to six-bit decimal number.
    """
    if ascii_code < 48 or 87 < ascii_code < 96 or ascii_code > 119:
        raise ValueError(f'Invalid ASCII {ascii_code}.')
    decimal = ascii_code - 48
    if decimal > 40:
        decimal -= 8
    return decimal


def convert_decimal_to_ascii_code(decimal_num: int) -> int:
    """
    Converts six-bit decimal number to ASCII code (AIVDM Payload Armoring).
    """
    if decimal_num < 0 or decimal_num > 63:
        raise ValueError('Wrong decimal number')
    if decimal_num not in range(33,40) and decimal_num + 8 > 40:
        decimal_num += 8
    ascii_code = decimal_num + 48
    return ascii_code


def add_padding(text: str, required_length: int, padding_char: str = ' ') -> str:
    """
    Adds padding to text if required.
    """
    if required_length < len(text):
        raise ValueError('The required length should not be greater than the length of the specified text')
    while len(text) < required_length:
        text += padding_char
    return text


def add_padding_0_bits(bits_string: str, required_length: int) -> tuple:
    """
    Adds 0 to bits string.
    Returns tuple - (bits string with padding, number of added 0s)
    """
    extra_0_bits_count = 0
    while len(bits_string) < required_length:
        bits_string += '0'
        extra_0_bits_count += 1
    return bits_string, extra_0_bits_count


def nmea_checksum(data: str) -> str:
    """
    Return calculated NMEA checksum.
    """
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


def convert_ais_payload_to_bits(payload: str) -> str:
    """
    Return string of bits from given AIS msg payload.
    """
    payload_bits = ''
    for char in payload:
        ascii_code = get_ascii_code_of_char(char)
        decimal = convert_ascii_code_to_decimal(ascii_code)
        payload_bits += convert_int_to_bits(decimal)
    return payload_bits
