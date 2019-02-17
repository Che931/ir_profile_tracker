from enum import Enum
from collections import OrderedDict


class Licence(Enum):
    """
    All licences available.
    """
    R = 1
    D = 2
    C = 3
    B = 4
    A = 5
    PRO = 6
    PRO_WC = 7


class RaceType(Enum):
    """
    Types of racing that iRacing supports.
    """
    Oval = 1
    Road = 2
    Dirt_Oval = 3
    Dirt_Road = 4


class SR(object):
    """
    Represents Safety Rating - class and value
    """
    def __init__(self, value=None):
        self._licence_class = Licence(1)
        self._number = 0.00

        if value:
            self.parse_from_int(value)

    def __str__(self):
        return "{0}{1}".format(self._licence_class.name, self._number)

    def parse_from_int(self, value):
        """
        Converts SR to class-number from a numeric value.
        SR is given as a four digit int where the most left is the class and the other 3 are the number.
        For example 5385 is  A3.85 or 3200 is C2.0.
        :param value: SR value as four digit number.
        :raise ValueError if SR value is not in range(0.00-4.99) or class is not in range(1-7).
        """
        licence = value // 1000
        number = ((value / 1000) % 1) * 10
        number = round(number, 2)

        if 0.00 <= number <= 4.99:
            self._number = number
        else:
            raise ValueError("{0} is not a valid SR number(0.00-4.99)".format(number))

        try:
            self._licence_class = Licence(licence)
        except ValueError as VE:
            raise ValueError("Licence number must be between 1-7. Your value {0}".format(licence)) from VE

    @property
    def number(self):
        """
        :return: Licence value and between 0.00 and 4.99
        """
        return self._number

    @property
    def licence_class(self):
        """
        :return: Class licence (R,D,C...)
        """
        return self._licence_class.name

    @property
    def licence_as_number(self):
        """
        :return: SR as integer. If class is A3.85, this method would return 5385
        """
        return int(self._licence_class.value * 1000 + self._number * 100)


class Member(object):
    """
    Represents a member
    """

    def __init__(self, custid, name):
        self.custid = custid
        self.name = name

        self._sr = OrderedDict((key, SR()) for key in RaceType)
        self._irating = OrderedDict((key, 0) for key in RaceType)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.custid)

    def update_sr(self, racetype, value):
        """
        Updates sr of one licence
        :param racetype: Racetype
        :param value: SR as int
        :raise ValueError if wrong value
        """
        self._sr[racetype].parse_from_int(value)

    def update_irating(self, racetype, irating):
        """
        Updates irating of one licence
        :param racetype: Racetype
        :param value: irating
        :raise ValueError if value is below 0 or not int.
        """
        if irating > 0 and type(irating) is int:
            self._irating[racetype] = irating
        else:
            raise ValueError("{0} is not a valid irating".format(irating))

    def irating_as_dict(self):
        """
        :return: A dict with the following structure: {Racetype: irating}
        """
        return self._irating.copy()

    def sr_as_dict(self):
        """
        :return: A dict with the following structure: {Racetype: SR object}
        """
        return self._sr.copy()

    @property
    def road_irating(self):
        return self._irating[RaceType.Road]

    @property
    def oval_irating(self):
        return self._irating[RaceType.Oval]

    @property
    def dRoad_irating(self):
        return self._irating[RaceType.Dirt_Road]

    @property
    def dOval_irating(self):
        return self._irating[RaceType.Dirt_Oval]

    @property
    def road_sr(self):
        return self._sr[RaceType.Road]

    @property
    def oval_sr(self):
        return self._sr[RaceType.Oval]

    @property
    def dOval_sr(self):
        return self._sr[RaceType.Dirt_Oval]

    @property
    def dRoad_sr(self):
        return self._sr[RaceType.Dirt_Road]

    @property
    def profile_url(self):
        return "http://members.iracing.com/membersite/member/CareerStats.do?custid={0}".format(self.custid)
