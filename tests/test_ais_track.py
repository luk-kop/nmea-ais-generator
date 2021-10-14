from ais_track import AISTrackList, ShipDimension


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


def test_ship_dimension_default_values_correct():
    dim = ShipDimension()
    assert dim.to_bow == 0
    assert dim.to_stern == 0
    assert dim.to_port == 0
    assert dim.to_starboard == 0


def test_ship_dimension_default_values_incorrect():
    dim = ShipDimension()
    assert dim.to_bow != 12
    assert dim.to_stern != 123
    assert dim.to_port != 12
    assert dim.to_starboard != 13