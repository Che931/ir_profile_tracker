import json
from unittest import TestCase
from unittest.mock import patch
from nose.tools import assert_equal, assert_raises
from ir_profile_tracker.irClient import IrClient, LOGIN_POST, LOGIN_GET, STATS_CHART
from ir_profile_tracker.models import RaceType


class TestiRClient(TestCase):

    def setUp(self):
        self.client = IrClient()
        self.memberid = 2020

    def test_login_valid_login(self):
        with patch.object(self.client, 'session') as session:

            session.get.return_value.status_code = 200
            session.post.return_value.status_code = 200
            session.cookies = {"cookie1": "value"}

            assert_equal(self.client.login('joe@example.com', 'password'), True)

            session.get.assert_called_once_with(LOGIN_GET)
            session.post.assert_called_once_with(LOGIN_POST, data={'username': 'joe@example.com', 'todaysdate': '',
                                                                   'utcoffset': 300, 'password': 'password'})

    def test_login_invalid_data_raise_exception(self):
        with patch.object(self.client, 'session') as session:

            session.get.return_value.status_code = 200
            session.post.return_value.status_code = 200
            session.cookies = {}

            with assert_raises(Exception):
                self.client.login('joe@example.com', 'password')

    def test_login_service_unavailable(self):
        with patch.object(self.client, 'session') as session:
            session.get.return_value.status_code = 404
            with assert_raises(Exception):
                self.client.login('joe@example.com', 'password')


    def test_get_SR_chart(self):
        with patch.object(self.client, 'session') as session:

            session.get.return_value.text = json.dumps([[102010, 4115], [102015, 4365]])
            sr = self.client.get_SR(memberid=self.memberid, racetype=RaceType.Road)

            assert_equal(sr, 4365)
            session.get.assert_called_once_with(STATS_CHART.format(self.memberid, RaceType.Road, 3))

    def test_get_SR_chart_return_None(self):
        with patch.object(self.client, 'session') as session:

            session.get.return_value.text = json.dumps([])
            sr = self.client.get_SR(memberid=self.memberid, racetype=RaceType.Road)

            session.get.assert_called_once_with(STATS_CHART.format(self.memberid, RaceType.Road, 3))
            assert_equal(sr, None)

    def test_get_SR_chart_raise_ValueError(self):
        with assert_raises(ValueError):
            self.client.get_SR(memberid=self.memberid, racetype=5)

    def test_get_irating_chart(self):
        with patch.object(self.client, 'session') as session:

            session.get.return_value.text = json.dumps([[102010, 2420], [102015, 3680]])
            ir = self.client.get_irating(memberid=self.memberid, racetype=RaceType.Road.value)

            assert_equal(ir, 3680)
            session.get.assert_called_once_with(STATS_CHART.format(self.memberid, RaceType.Road.value, 1))

    def test_get_irating_chart_raise_None(self):

        with patch.object(self.client, 'session') as session:
            session.get.return_value.text = json.dumps([])
            ir = self.client.get_irating(memberid=self.memberid, racetype=RaceType.Road.value)

            assert_equal(ir, None)
            session.get.assert_called_once_with(STATS_CHART.format(self.memberid, RaceType.Road.value, 1))

    def test_get_irating_chart_raise_ValueError(self):
        with assert_raises(ValueError):
            self.client.get_irating(memberid=self.memberid, racetype=5)
