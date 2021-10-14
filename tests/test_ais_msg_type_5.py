import pytest

from nmea_msg import ShipEta
from ais_track import ShipDimension

from nmea_utils import convert_ais_payload_to_bits


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
    # dim = ShipDimension(dimension_data=dummy_ship_dimension)
    dim = ShipDimension(**dummy_ship_dimension)
    assert dim.to_bow == 225
    assert dim.to_stern == 70
    assert dim.to_port == 1
    assert dim.to_starboard == 31


def test_ship_dimension_attrs_bits(dummy_ship_dimension):
    # dim = ShipDimension(dimension_data=dummy_ship_dimension)
    dim = ShipDimension(**dummy_ship_dimension)
    assert len(dim.bits) == 30
    assert dim.bits == '011100001001000110000001011111'


def test_ship_dimension_attrs_max(dummy_ship_dimension):
    # dim = ShipDimension(dimension_data=dummy_ship_dimension)
    dim = ShipDimension(**dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 600, 600, 100, 100
    assert dim.to_bow == 511
    assert dim.to_stern == 511
    assert dim.to_port == 63
    assert dim.to_starboard == 63


def test_ship_dimension_attrs_min(dummy_ship_dimension):
    # dim = ShipDimension(dimension_data=dummy_ship_dimension)
    dim = ShipDimension(**dummy_ship_dimension)
    dim.to_bow, dim.to_stern, dim.to_port, dim.to_starboard = 0, 0, 0, 0
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_ship_dimension_attrs_incorrect(dummy_ship_dimension):
    # dim = ShipDimension(dimension_data=dummy_ship_dimension)
    dim = ShipDimension(**dummy_ship_dimension)
    with pytest.raises(Exception):
        dim.to_bow = -1
    with pytest.raises(Exception):
        dim.to_stern = -1
    with pytest.raises(Exception):
        dim.to_port = -1
    with pytest.raises(Exception):
        dim.to_starboard = -1


def test_aismsg_eta(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.eta) == 20
    assert msg.eta == '01010111101110000000'


def test_ship_eta_attrs(dummy_ship_eta):
    eta = ShipEta(eta_data=dummy_ship_eta)
    assert eta.month == 5
    assert eta.day == 15
    assert eta.hour == 14
    assert eta.minute == 0


def test_ship_eta_attrs_bits(dummy_ship_eta):
    eta = ShipEta(eta_data=dummy_ship_eta)
    assert len(eta.bits) == 20
    assert eta.bits == '01010111101110000000'


def test_ship_eta_attrs_max(dummy_ship_eta):
    eta = ShipEta(eta_data=dummy_ship_eta)
    eta.month, eta.day, eta.hour, eta.minute = 12, 31, 24, 60
    assert eta.month == 12
    assert eta.day == 31
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_min(dummy_ship_eta):
    eta = ShipEta(eta_data=dummy_ship_eta)
    eta.month, eta.day, eta.hour, eta.minute = 0, 0, 0, 0
    assert eta.month == 0
    assert eta.day == 0
    assert eta.hour == 0
    assert eta.minute == 0


def test_ship_eta_attrs_min_incorrect(dummy_ship_eta):
    eta = ShipEta(eta_data=dummy_ship_eta)
    with pytest.raises(Exception):
        eta.month = -1
    with pytest.raises(Exception):
        eta.day = -1
    with pytest.raises(Exception):
        eta.hour = -1
    with pytest.raises(Exception):
        eta.minute = -1


def test_ship_eta_attrs_not_present():
    eta = ShipEta(eta_data={})
    assert eta.month == 0
    assert eta.day == 0
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_some_not_present():
    eta_data = {
        'month': 12,
        'day': 10
    }
    eta = ShipEta(eta_data=eta_data)
    assert eta.month == 12
    assert eta.day == 10
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_incorrect_keys():
    eta_data = {
        'month': 12,
        'xxx': 10,
        'qqq': 'www'
    }
    eta = ShipEta(eta_data=eta_data)
    assert eta.month == 12
    assert eta.day == 0
    assert eta.hour == 24
    assert eta.minute == 60


def test_aismsg_draught(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.draught) == 8
    assert msg.draught == '01111010'


def test_aismsg_draught_min(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.draught = 0
    assert msg.draught == '00000000'


def test_aismsg_draught_max(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.draught = 25.5
    assert msg.draught == '11111111'


def test_aismsg_draught_above_max(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.draught = 100
    assert msg.draught == '11111111'


def test_aismsg_draught_above_incorrect(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    with pytest.raises(Exception):
        msg.draught = -1


def test_aismsg_destination(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.destination) == 120
    assert msg.destination == '001110000101010111100000011001001111010010001011100000100000100000100000100000' \
                              '100000100000100000100000100000100000100000'


def test_aismsg_destination_empty(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    msg.destination = ''
    assert len(msg.destination) == 120
    assert msg.destination == '000000' * 20


def test_aismsg_before_encode(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert msg.fill_bits == 0
    assert len(msg.payload_bits) == 424


def test_aismsg_after_encode_fill_bits(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    ais_payload = msg.encode()
    # payload with fill-bits added
    assert msg.fill_bits == 2


def test_aismsg_after_encode_payload_chars_length(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    ais_payload = msg.encode()
    # payload with fill-bits added
    assert len(ais_payload) == 71


def test_aismsg_after_encode_payload_bits_length(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    ais_payload = msg.encode()
    # payload with fill-bits added
    payload_bits = convert_ais_payload_to_bits(payload=ais_payload)
    assert len(payload_bits) == 426


def test_aismsg_after_encode_payload_content(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    ais_payload = msg.encode()
    # payload with fill-bits added
    assert ais_payload == '533m@o`2;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880'