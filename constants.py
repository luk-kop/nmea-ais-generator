from enum import IntEnum


class MmsiCountryEnum(IntEnum):
    """
    Maritime Identification Digits (MID). Only selected countries are listed.
    For all codes see: https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/mid.aspx
    """
    Belgium = 205
    Germany = 211
    Denmark = 219
    Spain = 224
    France = 226
    Finland = 230
    UK = 232
    Greece = 237
    Netherlands = 244
    Italy = 247
    Ireland = 250
    Iceland = 251
    Norway = 257
    Poland = 261
    Portugal = 263
    Romania = 264
    Sweden = 265
    Turkey = 271
    Ukraine = 272
    RussianFederation = 273
    Latvia = 275
    Estonia = 276
    Lithuania = 277
    Slovenia = 278
    Bahamas = 311
    Canada = 316
    USA = 338

    @classmethod
    def has_value(cls, value):
        values = set(item.value for item in cls)
        return value in values


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
    def has_value(cls, value):
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
    def has_value(cls, value):
        values = set(item.value for item in cls)
        return value in values