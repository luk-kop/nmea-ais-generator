from enum import IntEnum
from typing import Dict, List

from aenum import MultiValueEnum


class MmsiCountryEnum(MultiValueEnum):
    """
    Maritime Identification Digits (MID). Only selected countries are listed.
    For all codes see: https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/mid.aspx
    """
    Antigua_Barbuda = 305
    Bahamas = 308, 309, 311
    Belgium = 205
    Canada = 316
    Germany = 211, 218
    Denmark = 219, 220
    Spain = 224, 225
    France = 226, 227, 228
    Finland = 230
    UK = 232, 233, 234, 235
    Greece = 237, 239, 240, 241
    Netherlands = 244, 245, 246
    Italy = 247
    Ireland = 250
    Iceland = 251
    Malta = 248, 249
    Norway = 257, 258, 259
    Poland = 261
    Portugal = 263
    Romania = 264
    Sweden = 265, 266
    Turkey = 271
    Ukraine = 272
    Russian_Federation = 273
    Latvia = 275
    Estonia = 276
    Lithuania = 277
    Slovenia = 278
    USA = 338, 366, 367, 368, 369

    @classmethod
    def has_value(cls, value) -> bool:
        values = cls.all_values()
        return value in values

    @classmethod
    def all_values(cls) -> List[int]:
        """
        Returns all item values (including muliti-values).
        """
        values_list_of_tuples = [item.values for item in cls]
        values = []
        for values_tuple in values_list_of_tuples:
            for value in values_tuple:
                values.append(value)
        # One-liner example:
        # values = [value for values_tuple in [item.values for item in cls] for value in values_tuple]
        return values


class NavigationStatusEnum(IntEnum):
    """
    Navigational status for AIS msg type 1.
    """
    Under_way_using_engine = 0
    At_anchor = 1
    Not_under_command = 2
    Restricted_manoeuverability = 3
    Constrained_by_her_draught = 4
    Moored = 5
    Aground = 6
    Engaged_in_fishing = 7
    Under_way_sailing = 8
    AISSART_active = 14
    Undefined = 15

    @classmethod
    def has_value(cls, value) -> bool:
        values = set(item.value for item in cls)
        return value in values


class ShipTypeEnum(IntEnum):
    """
    Ship type codes for AIS msg type 5. Only selected ship types are listed.
    For all codes see: https://gpsd.gitlab.io/gpsd/AIVDM.html#_aivdmaivdo_sentence_layer
    """
    Not_available = 0
    # 30's
    Wing_in_ground = 20
    Fishing = 30
    Towing = 31
    Towing_length_over_200m = 32
    Dredging_or_underwater_ops = 33
    Diving_ops = 34
    Military_ops = 35
    Sailing = 36
    Pleasure_craft = 37
    High_speed_craft = 40
    Pilot_vessel = 50
    SAR_vessel = 51
    Tug = 52
    Port_tender = 53
    Anti_pollution_equipment = 54
    Law_enforcement = 55
    Medical_transport = 58
    Non_combat_ship = 59
    Passenger = 60
    Cargo = 70
    Tanker = 80
    Other_type = 90

    @classmethod
    def has_value(cls, value) -> bool:
        values = set(item.value for item in cls)
        return value in values


class AISMsgType1ConstsEnum(IntEnum):
    """
    Constant data for AIS msg type 1.
    """
    maneuver = 0
    msg_type = 1
    # Position accuracy - high (1)
    pos_accuracy = 1
    # RAIM - not in use (0)
    raim = 0
    # ROT - default value, no turn info available (128)
    rot = 128
    spare_type_1 = 0
    # Dummy SOTDMA data - bits '0010100000111110011'
    radio_status = 82419

    @classmethod
    def dict(cls) -> Dict[str, int]:
        return {k: v.value for k, v in cls.__members__.items()}


class AISMsgType5ConstsEnum(IntEnum):
    """
    Constant data for AIS msg type 5.
    """
    msg_type = 5
    ais_version = 2
    pos_fix_type = 1
    dte = 0
    spare_type_5 = 0

    @classmethod
    def dict(cls) -> Dict[str, int]:
        return {k: v.value for k, v in cls.__members__.items()}


class FieldBitsCountEnum(IntEnum):
    """
    Bits count for AIS msg fields.
    """
    mmsi = 30
    repeat_indicator = 2
    msg_type = 6
    nav_status = 4
    rot = 8
    speed = 10
    pos_accuracy = 1
    lon = 28
    lat = 27
    course = 12
    true_heading = 9
    timestamp = 6
    maneuver = 2
    spare_type_1 = 3
    spare_type_5 = 1
    raim = 1
    radio_status = 19
    ais_version = 2
    imo = 30
    call_sign = 42
    ship_name = 120
    ship_type = 8
    pos_fix_type = 4
    draught = 8
    destination = 120
    dte = 1

    @classmethod
    def dict(cls) -> Dict[str, int]:
        return {k: v.value for k, v in cls.__members__.items()}


class FieldCharsCountEnum(IntEnum):
    """
    Chars count for AIS msg fields.
    """
    mmsi = 9
    imo = 7
    call_sign = 7
    ship_name = 20
    destination = 20

