from ais_utils import get_first_3_digits, check_mmsi_mid_code, verify_imo


def test_get_first_3_digits():
    value = 123456789
    result = get_first_3_digits(value)
    assert result == 123


def test_check_mmsi_mid_code_true():
    value = 205344990
    result = check_mmsi_mid_code(value)
    assert result is True


def test_check_mmsi_mid_code_false():
    value = 123344990
    result = check_mmsi_mid_code(value)
    assert result is False


def test_verify_imo_correct():
    imo_values = [9134270, 7625811, 9736872]
    for imo in imo_values:
        assert verify_imo(imo) is True