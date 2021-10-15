from constants import MmsiCountry


def test_mmsi_country_has_value_true():
    assert MmsiCountry.has_value(261) is True
    assert MmsiCountry.has_value(211) is True


def test_mmsi_country_has_value_false():
    assert MmsiCountry.has_value(1) is False
    assert MmsiCountry.has_value(2) is False
