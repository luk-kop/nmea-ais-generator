from constants import MmsiCountryEnum


def test_mmsi_country_has_value_true():
    assert MmsiCountryEnum.has_value(261) is True
    assert MmsiCountryEnum.has_value(211) is True


def test_mmsi_country_has_value_false():
    assert MmsiCountryEnum.has_value(1) is False
    assert MmsiCountryEnum.has_value(2) is False
