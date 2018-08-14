from enum import Enum


class RiskTypes(Enum):
    AM = 'automobile'
    HO = 'house'
    PR = 'prize'


class DataTypes(Enum):
    # text, number, date, or enum
    TE = 'text'
    NU = 'number'
    DA = 'date'
    EN = 'enum'
