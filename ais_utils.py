from constants import MmsiCountry


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
    return MmsiCountry.has_value(country_code)


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

