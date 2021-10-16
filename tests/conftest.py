from pytest import fixture

from nmea_msg import AISMsgType1, AISMsgType5
from ais_utils import ShipDimension, ShipEta


@fixture
def dummy_ship_dimension():
    dimension_dict = {
        'to_bow': 225,
        'to_stern': 70,
        'to_port': 1,
        'to_starboard': 31
    }
    return dimension_dict


@fixture
def dummy_ship_eta():
    eta_dict = {
        'month': 5,
        'day': 15,
        'hour': 14,
        'minute': 0
    }
    return eta_dict


@fixture
def dummy_ais_msg_type_5(dummy_ship_dimension, dummy_ship_eta):
    msg = AISMsgType5(mmsi=205344990,
                      imo=9134270,
                      call_sign='3FOF8',
                      ship_name='EVER DIADEM',
                      ship_type=70,
                      dimension=ShipDimension(**dummy_ship_dimension),
                      eta=ShipEta(**dummy_ship_eta),
                      draught=12.2,
                      destination='NEW YORK')
    return msg


@fixture
def dummy_ais_msg_type_1():
    msg = AISMsgType1(mmsi=205344990,
                      speed=0,
                      course=110.7,
                      lon=4.407046666667,
                      lat=51.229636666667,
                      nav_status=15,
                      timestamp=40)
    return msg


@fixture
def dummy_ais_tracks_list_single(dummy_ship_dimension, dummy_ship_eta):
    tracks = [
        {
            'mmsi': 205344990,
            'nav_status': 15,
            'lon': 4.407046666667,
            'lat': 51.229636666667,
            'speed': 0,
            'course': 110.7,
            'imo': 9134270,
            'call_sign': '3FOF8',
            'ship_name': 'EVER DIADEM',
            'ship_type': 70,
            'dimension': dummy_ship_dimension,
            'eta': dummy_ship_eta,
            'draught': 12.2,
            'destination': 'NEW YORK',
            'timestamp': 40
        }
    ]
    return tracks
