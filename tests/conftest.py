from pytest import fixture

from main import AisMsgType5


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
    msg = AisMsgType5(mmsi=205344990,
                      imo=9134270,
                      call_sign='3FOF8',
                      ship_name='EVER DIADEM',
                      ship_type=70,
                      dimension=dummy_ship_dimension,
                      eta=dummy_ship_eta,
                      draught=12.2,
                      destination='NEW YORK')
    return msg
