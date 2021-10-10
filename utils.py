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


def convert_int_to_bits(num: int, bits_count: int = 6) -> str:
    """
    Converts int to bits string.
    """
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