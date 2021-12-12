from ais.constants import MmsiCountryEnum


def test_mmsi_country_has_value_true():
    assert MmsiCountryEnum.has_value(261) is True
    assert MmsiCountryEnum.has_value(211) is True


def test_mmsi_country_has_value_false():
    assert MmsiCountryEnum.has_value(1) is False
    assert MmsiCountryEnum.has_value(2) is False


def test_mmsi_country_has_value_multi_values():
    assert MmsiCountryEnum.has_value(308) is True
    assert MmsiCountryEnum.has_value(309) is True
    assert MmsiCountryEnum.has_value(311) is True
    assert MmsiCountryEnum.has_value(227) is True
    assert MmsiCountryEnum.has_value(240) is True
    assert MmsiCountryEnum.has_value(368) is True
    assert MmsiCountryEnum.has_value(369) is True
