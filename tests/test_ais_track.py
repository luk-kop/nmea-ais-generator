import pytest

from ais_track import AISTrackList, ShipDimension, ShipEta


def test_ais_track_list_single(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    assert len(track_list.tracks) == 1
    assert track_list.dict()['tracks'] == dummy_ais_tracks_list_single


def test_ais_track_list_single_attrs(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.mmsi == 205344990
    assert track.nav_status == 15
    assert track.lon == 4.407046666667
    assert track.lat == 51.229636666667
    assert track.speed == 0
    assert track.course == 110.7
    assert track.imo == 9134270
    assert track.call_sign == '3FOF8'
    assert track.ship_name == 'EVER DIADEM'
    assert track.ship_type == 70
    assert track.dimension == {
        'to_bow': 225,
        'to_stern': 70,
        'to_port': 1,
        'to_starboard': 31
    }
    assert track.eta == {
        'month': 5,
        'day': 15,
        'hour': 14,
        'minute': 0
    }
    assert track.draught == 12.2
    assert track.destination == 'NEW YORK'


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


def test_ship_eta_attrs(dummy_ship_eta):
    eta = ShipEta(**dummy_ship_eta)
    assert eta.month == 5
    assert eta.day == 15
    assert eta.hour == 14
    assert eta.minute == 0


def test_ship_eta_attrs_bits(dummy_ship_eta):
    eta = ShipEta(**dummy_ship_eta)
    assert len(eta.bits) == 20
    assert eta.bits == '01010111101110000000'


def test_ship_eta_attrs_max(dummy_ship_eta):
    eta = ShipEta(**dummy_ship_eta)
    eta.month, eta.day, eta.hour, eta.minute = 12, 31, 24, 60
    assert eta.month == 12
    assert eta.day == 31
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_min(dummy_ship_eta):
    eta = ShipEta(**dummy_ship_eta)
    eta.month, eta.day, eta.hour, eta.minute = 0, 0, 0, 0
    assert eta.month == 0
    assert eta.day == 0
    assert eta.hour == 0
    assert eta.minute == 0


def test_ship_eta_attrs_min_incorrect(dummy_ship_eta):
    eta = ShipEta(**dummy_ship_eta)
    with pytest.raises(Exception):
        eta.month = -1
    with pytest.raises(Exception):
        eta.day = -1
    with pytest.raises(Exception):
        eta.hour = -1
    with pytest.raises(Exception):
        eta.minute = -1


def test_ship_eta_attrs_some_not_present():
    eta_data = {
        'month': 12,
        'day': 10
    }
    eta = ShipEta(**eta_data)
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
    eta = ShipEta(**eta_data)
    assert eta.month == 12
    assert eta.day == 0
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_default_values_correct():
    eta = ShipEta()
    assert eta.month == 0
    assert eta.day == 0
    assert eta.hour == 24
    assert eta.minute == 60


def test_ship_eta_attrs_default_values_incorrect():
    eta = ShipEta()
    assert eta.month != 1
    assert eta.day != 1
    assert eta.hour != 0
    assert eta.minute != 0