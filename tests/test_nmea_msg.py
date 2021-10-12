from main import NMEAMessage


def test_nmea_msg_multi_sentence(dummy_ais_msg_type_5):
    nmea_msg = NMEAMessage(payload=dummy_ais_msg_type_5)
    test_sentences = [
        '!AIVDM,2,1,1,A,533m@o`2;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*7D\r\n',
        '!AIVDM,2,2,1,A,88888888880,2*25\r\n'
    ]
    assert nmea_msg.get_sentences() == test_sentences


def test_nmea_msg_single_sentence(dummy_ais_msg_type_1):
    nmea_msg = NMEAMessage(payload=dummy_ais_msg_type_1)
    test_sentences = [
        '!AIVDM,1,1,,A,133m@ogP00PD;88MD5MTDww@0D7k,0*44\r\n'
    ]
    assert nmea_msg.get_sentences() == test_sentences


