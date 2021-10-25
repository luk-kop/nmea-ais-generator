import pytest

from ais_track import AISTrackList, ShipEta
from nmea_msg import AISMsgPayloadType1, AISMsgPayloadType5


def test_ais_track_list_single(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    assert len(track_list.tracks) == 1


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
    assert track.call_sign == '3FOF8  '
    assert track.ship_name == 'EVER DIADEM' + ' ' * 9
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
    assert track.destination == 'NEW YORK' + ' ' * 12
    assert track.timestamp == 40


def test_ais_track_attr_mmsi_correct(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['mmsi'] = 261000001
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.mmsi == 261000001


def test_ais_track_attr_mmsi_incorrect_mid(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    with pytest.raises(Exception):
        track.mmsi = 123000001


def test_ais_track_attr_mmsi_incorrect_len(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    with pytest.raises(Exception):
        track.mmsi = 12300000


def test_ais_track_attr_nav_status_correct(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['nav_status'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.nav_status == 0


def test_ais_track_attr_nav_status_incorrect(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['nav_status'] = 30
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_lon_correct(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lon'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.lon == 0


def test_ais_track_attr_lon_correct_multiple(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lon'] = 10
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    for lon in [-180, -10, 10, 180]:
        track.lon = lon
        assert track.lon == lon


def test_ais_track_attr_lon_incorrect_str(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lon'] = 'xxx'
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_lon_incorrect_value(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lon'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    with pytest.raises(Exception):
        track.lon = -200
    with pytest.raises(Exception):
        track.lon = 200


def test_ais_track_attr_lat_correct(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lat'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.lat == 0


def test_ais_track_attr_lat_correct_multiple(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lat'] = 10
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    for lat in [-90, -10, 10, 90]:
        track.lat = lat
        assert track.lat == lat


def test_ais_track_attr_lat_incorrect_str(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lat'] = 'xxx'
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_lat_incorrect_value(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['lat'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    with pytest.raises(Exception):
        track.lat = -91
    with pytest.raises(Exception):
        track.lat = 92


def test_ais_track_attr_speed_min(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['speed'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.speed == 0


def test_ais_track_attr_speed_max(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['speed'] = 102.2
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.speed == 102.2


def test_ais_track_attr_speed_incorrect_above(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['speed'] = 105
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_speed_incorrect_below(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['speed'] = -1
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_course_min(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['course'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.course == 0


def test_ais_track_attr_course_max(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['course'] = 360
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.course == 360


def test_ais_track_attr_course_incorrect_above(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['course'] = 361
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_course_incorrect_below(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['course'] = -1
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_true_heading_default(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.true_heading == 511


def test_ais_track_attr_true_heading_min(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['course'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.course == 0


def test_ais_track_attr_true_heading_max(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['true_heading'] = 360
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.true_heading == 360


def test_ais_track_attr_true_heading_incorrect_above(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['true_heading'] = 361
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_true_heading_incorrect_below(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['true_heading'] = -1
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_imo(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['imo'] = 9134270
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.imo == 9134270


def test_ais_track_attr_imo_too_short(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['imo'] = 91342
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_imo_invalid(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['imo'] = 1234271
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_call_sign(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['call_sign'] = 'SQWD'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.call_sign == 'SQWD   '


def test_ais_track_attr_call_sign_long(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['call_sign'] = '1234567890'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.call_sign == '1234567'


def test_ais_track_attr_call_sign_incorrect(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['call_sign'] = 'sqWD'
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_ship_name(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['ship_name'] = 'STORM'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.ship_name == 'STORM' + ' ' * 15


def test_ais_track_attr_ship_name_long(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['ship_name'] = 'THE QUICK BROWN FOX JUMPS OVER'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.ship_name == 'THE QUICK BROWN FOX '


def test_ais_track_attr_ship_name_incorrect(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['ship_name'] = 'sToRM'
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_ship_type_correct(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['ship_type'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.ship_type == 0


def test_ais_track_attr_ship_type_incorrect(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['ship_type'] = 100
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_draught_min(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['draught'] = 0
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.draught == 0


def test_ais_track_attr_draught_max(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['draught'] = 25.5
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.draught == 25.5


def test_ais_track_attr_draught_above(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['draught'] = 30
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.draught == 25.5


def test_ais_track_attr_draught_incorrect_below(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['draught'] = -1
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_destination(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['destination'] = 'BORNHOLM'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.destination == 'BORNHOLM' + ' ' * 12


def test_ais_track_attr_destination_long(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['destination'] = 'THE QUICK BROWN FOX JUMPS OVER'
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.destination == 'THE QUICK BROWN FOX '


def test_ais_track_attr_destination_incorrect(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['destination'] = 'BOrNHOLM'
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_timestamp_min(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['timestamp'] = 40
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.timestamp == 40


def test_ais_track_attr_timestamp_max(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['timestamp'] = 60
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.timestamp == 60


def test_ais_track_attr_timestamp_incorrect_above(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['timestamp'] = 61
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


def test_ais_track_attr_timestamp_incorrect_below(dummy_ais_tracks_list_single):
    dummy_ais_tracks_list_single[0]['timestamp'] = -1
    with pytest.raises(Exception):
        track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)


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


def test_generate_payload_type_1_type(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert isinstance(track.generate_payload_type_1(), AISMsgPayloadType1)


def test_generate_payload_type_1_encode(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.generate_payload_type_1().encode() == '133m@ogP00PD;88MD5MTDww@0D7k'


def test_generate_payload_type_5_type(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert isinstance(track.generate_payload_type_5(), AISMsgPayloadType5)


def test_generate_payload_type_5_encode(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    assert track.generate_payload_type_5().encode() == '533m@o`2;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp888888888880'


def test_generate_nmea_list_of_str(dummy_ais_tracks_list_single):
    track_list = AISTrackList(tracks=dummy_ais_tracks_list_single)
    track = track_list.tracks[0]
    for msg in track.generate_nmea():
        assert isinstance(msg, str)




