from unittest import TestCase
from nose.tools import assert_equal, assert_raises, assert_list_equal
from ir_profile_tracker.models import Member, SR, RaceType


class TestSR(TestCase):

    def setUp(self):
        self.sr = SR(4365)

    def test_str(self):
        assert_equal(str(self.sr), "B3.65")

    def test_parse_from_int(self):
        self.sr.parse_from_int(5499)

        assert_equal(self.sr.licence_class, 'A')
        assert_equal(self.sr.number, 4.99)

    def test_parse_licence_wrong_value_raise_exception(self):
        with assert_raises(ValueError):
            self.sr.parse_from_int(8499)

    def test_wrong_number_raise_exception(self):
        with assert_raises(ValueError):
            self.sr.parse_from_int(8599)

    def test_licence_as_number(self):
        assert_equal(self.sr.licence_as_number, 4365)


class TestMember(TestCase):

    def setUp(self):
        self.member = Member(custid=2020, name="John Doe")

    def test_str(self):
        assert_equal(self.member.__str__(), "John Doe - 2020")

    def test_update_sr_wrong_value(self):
        with assert_raises(ValueError):
            self.member.update_sr(RaceType.Oval, 9268)

    def test_update_irating_wrong_value(self):
            with assert_raises(ValueError):
                self.member.update_irating(RaceType.Oval, 3750.25)

    def test_road_ir_property(self):
        value = 3000
        self.member.update_irating(RaceType.Road, value)
        assert_equal(self.member.road_irating, value)

    def test_droad_ir_property(self):
        value = 3800
        self.member.update_irating(RaceType.Dirt_Road, value)
        assert_equal(self.member.dRoad_irating, value)

    def test_oval_ir_property(self):
        value = 500
        self.member.update_irating(RaceType.Oval, value)
        assert_equal(self.member.oval_irating, value)

    def test_doval_ir_property(self):
        value = 1800
        self.member.update_irating(RaceType.Dirt_Oval, value)
        assert_equal(self.member.dOval_irating, value)

    def test_road_sr_property(self):
        value = 5499

        self.member.update_sr(RaceType.Road, value)
        assert_equal(self.member.road_sr.number, 4.99)
        assert_equal(self.member.road_sr.licence_class, 'A')

    def test_droad_sr_property(self):
        value = 5475

        self.member.update_sr(RaceType.Dirt_Road, value)
        assert_equal(self.member.dRoad_sr.number, 4.75)
        assert_equal(self.member.dRoad_sr.licence_class, 'A')

    def test_oval_sr_property(self):
        value = 2222

        self.member.update_sr(RaceType.Oval, value)
        assert_equal(self.member.oval_sr.number, 2.22)
        assert_equal(self.member.oval_sr.licence_class, 'D')

    def test_doval_sr_property(self):
        value = 7350

        self.member.update_sr(RaceType.Dirt_Oval, value)
        assert_equal(self.member.dOval_sr.number, 3.50)
        assert_equal(self.member.dOval_sr.licence_class, 'PRO_WC')

    def test_irating_as_dict(self):
        ir_expected = [1000, 2500, 3850, 6200]

        for item in range(0, 4):
            self.member.update_irating(RaceType(item+1), ir_expected[item])

        values = [item for item in self.member.irating_as_dict().values()]
        assert_list_equal(ir_expected, values)

    def test_sr_as_dict(self):
        sr_expected = [2342, 4365, 5499, 2128]

        for item in range(0, 4):
            self.member.update_sr(RaceType(item+1), sr_expected[item])

        values = [item.licence_as_number for item in self.member.sr_as_dict().values()]
        assert_list_equal(sr_expected, values)
