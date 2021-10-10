import pytest

from main import ShipDimension


def test_aismsg_mmsi(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.mmsi) == 30
    assert msg.mmsi == '001100001111010101000011011110'


def test_aismsg_imo(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.imo) == 30
    assert msg.imo == '000000100010110110000010111110'


def test_aismsg_call_sign(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.call_sign) == 42
    assert msg.call_sign == '110011000110001111000110111000100000100000'


def test_aismsg_call_sign_empty(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.call_sign = ''
    assert len(msg.call_sign) == 42
    assert msg.call_sign == '000000' * 7


def test_aismsg_ship_name(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.ship_name) == 120
    assert msg.ship_name == '000101010110000101010010100000000100001001000001000100000101001101100000100000100000' \
                            '100000100000100000100000100000100000'


def test_aismsg_ship_name_empty(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.ship_name = ''
    assert len(msg.ship_name) == 120
    assert msg.ship_name == '000000' * 20


def test_aismsg_ship_type(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.ship_type) == 8
    assert msg.ship_type == '01000110'


def test_aismsg_dimension(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.dimension) == 30
    assert msg.dimension == '011100001001000110000001011111'


def test_ship_dimension_attrs(dummy_ship_dimension):
    dim = ShipDimension(dimension=dummy_ship_dimension)
    assert dim.to_bow == 225
    assert dim.to_stern == 70
    assert dim.to_port == 1
    assert dim.to_starboard == 31


def test_ship_dimension_attrs_bits(dummy_ship_dimension):
    dim = ShipDimension(dimension=dummy_ship_dimension)
    assert len(dim.bits) == 30
    assert dim.bits == '011100001001000110000001011111'


def test_ship_dimension_attrs_max(dummy_ship_dimension):
    dim = ShipDimension(dimension=dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 600, 600, 100, 100
    assert dim.to_bow == 511
    assert dim.to_stern == 511
    assert dim.to_port == 63
    assert dim.to_starboard == 63


def test_ship_dimension_attrs_min(dummy_ship_dimension):
    dim = ShipDimension(dimension=dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 0, 0, 0, 0
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_ship_dimension_attrs_incorrect(dummy_ship_dimension):
    dim = ShipDimension(dimension=dummy_ship_dimension)
    with pytest.raises(Exception):
        dim.to_bow = -1
    with pytest.raises(Exception):
        dim.to_stern = -1
    with pytest.raises(Exception):
        dim.to_port = -1
    with pytest.raises(Exception):
        dim.to_starboard = -1
