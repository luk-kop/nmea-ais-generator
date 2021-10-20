from datetime import datetime

import pytest

from ais_utils import (
    get_first_3_digits,
    check_mmsi_mid_code,
    verify_imo, ShipDimension,
    calculate_distance,
    calculate_new_position
)


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


def test_ship_dimension_attrs(dummy_ship_dimension):
    dim = ShipDimension(**dummy_ship_dimension)
    assert dim.to_bow == 225
    assert dim.to_stern == 70
    assert dim.to_port == 1
    assert dim.to_starboard == 31


def test_ship_dimension_attrs_bits(dummy_ship_dimension):
    dim = ShipDimension(**dummy_ship_dimension)
    assert len(dim.bits) == 30
    assert dim.bits == '011100001001000110000001011111'


def test_ship_dimension_attrs_max(dummy_ship_dimension):
    dim = ShipDimension(**dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 600, 600, 100, 100
    assert dim.to_bow == 511
    assert dim.to_stern == 511
    assert dim.to_port == 63
    assert dim.to_starboard == 63


def test_ship_dimension_attrs_min(dummy_ship_dimension):
    dim = ShipDimension(**dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 0, 0, 0, 0
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_ship_dimension_attrs_incorrect(dummy_ship_dimension):
    dim = ShipDimension(**dummy_ship_dimension)
    with pytest.raises(Exception):
        dim.to_bow = -1
    with pytest.raises(Exception):
        dim.to_stern = -1
    with pytest.raises(Exception):
        dim.to_port = -1
    with pytest.raises(Exception):
        dim.to_starboard = -1


def test_ship_dimension_attrs_default_values_correct():
    dim = ShipDimension()
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_ship_dimension_attrs_default_values_incorrect():
    dim = ShipDimension()
    assert dim.to_bow != 12
    assert dim.to_stern != 123
    assert dim.to_port != 12
    assert dim.to_starboard != 13


def test_ship_dimension_attrs_omitted():
    dimension_dict = {
        'to_bow': 123,
        'to_starboard': 23
    }
    dim = ShipDimension(**dimension_dict)
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_calculate_distance():
    # Use the last_timestamp 60 seconds before the current_timestamp
    current_timestamp = datetime.utcnow().timestamp()
    last_timestamp = current_timestamp - 60
    distance = calculate_distance(last_timestamp=last_timestamp, current_timestamp=current_timestamp, speed=10)
    assert distance == 308.667


def test_calculate_new_position():
    lon_new, lat_new = calculate_new_position(lon_start=-71.-(7./60.),
                                              lat_start=42.+(15./60.),
                                              course=-66.531,
                                              distance=4164192.708)
    assert round(lon_new, 3) == -123.685
    assert round(lat_new, 3) == 45.516
