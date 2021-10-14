import pytest

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


def test_aismsg_eta(dummy_ais_msg_type_5):
    msg = dummy_ais_msg_type_5
    assert len(msg.eta) == 20
    assert msg.eta == '01010111101110000000'


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