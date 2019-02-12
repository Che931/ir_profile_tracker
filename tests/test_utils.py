from unittest import TestCase
from unittest import mock
import json
from datetime import datetime
from nose.tools import assert_equal, assert_raises, assert_list_equal, assert_true
from ir_profile_tracker import utils
from ir_profile_tracker.models import Member


class TestExportCSV(TestCase):

    def setUp(self):
        self.member = Member(name="John Doe", custid=2020)

    def get_write_calls_arg(self, mock_calls, index):
        """
        Bypass to get all args from every write call when csv file is being writed. I tried all assert methods from mock
        module but I did something wrong so, this method allows me to check if file constains the right info.

        :param mock_calls: mock.mock_calls array
        :param index: Index in the mock_calls array
        :return: Array with all args as str.
        """
        calls = [item[1][0] for item in mock_calls if item[0] == "().__enter__().write"]
        call = calls[index]
        args = call.replace('\n', '').replace('\r', '')
        return args.split(',')

    @mock.patch("builtins.open")
    def test_drivers_to_csv_member_info(self, mock_open):
        driver_expected_args = [self.member.name, self.member.custid, self.member.road_irating,
                                self.member.oval_irating, self.member.dRoad_irating, self.member.dOval_irating,
                                self.member.road_sr, self.member.oval_sr, self.member.dRoad_sr,
                                self.member.dOval_sr, self.member.profile_url]

        utils.drivers_to_csv([self.member])

        drivers_call_args = self.get_write_calls_arg(mock_open.mock_calls, 1)

        mock_open.assert_called_once_with("driversStats.csv", "w")
        assert_list_equal(drivers_call_args, [str(item) for item in driver_expected_args])

    @mock.patch("builtins.open")
    @mock.patch("ir_profile_tracker.utils.datetime")
    def test_drivers_to_csv_created_date(self, mock_dt, mock_open):
        today = datetime(2019, 2, 4, 1, 0, 0, 0)
        mock_dt.utcnow.return_value = today

        utils.drivers_to_csv([self.member])
        date_call_args = self.get_write_calls_arg(mock_open.mock_calls, 3)
        assert_equal(date_call_args[0], "Created: " + today.strftime("%d-%b-%Y %H:%M:%S UTC"))

    @mock.patch("builtins.open")
    def test_drivers_to_csv_file_headers(self, mock_open):
        utils.drivers_to_csv([self.member])

        headers_call_args = self.get_write_calls_arg(mock_open.mock_calls, 0)
        headers_expected = ['Name', 'Id', 'ir-Road', 'ir-Oval', 'ir-DRoad', 'ir-DOval', 'sr-Road', 'sr-Oval',
                            'sr-DRoad', 'sr-DOval', 'Profile']

        assert_list_equal(headers_call_args, headers_expected)

    @mock.patch("builtins.open")
    def test_drivers_to_csv_custom_file(self, mock_os):
        filename = "myfile.csv"
        utils.drivers_to_csv([self.member], filename)
        mock_os.assert_called_once_with(filename, "w")

    @mock.patch("builtins.open")
    def test_drivers_to_csv_custom_file_error(self, mock_os):
        filename = "output/myfile.csv"
        mock_os.side_effect = IOError()

        with assert_raises(IOError):
            utils.drivers_to_csv([self.member], filename)


class TestUtils(TestCase):

    @mock.patch('ir_profile_tracker.utils.time.sleep', return_value=None)
    def test_update_drivers(self, mock_time):
        member = Member(name="John Doe", custid=2020)
        client = mock.Mock()
        ir_list = [1000, 1500, 3000, 2500]
        sr_list = [2342, 4365, 5499, 2128]

        client.get_irating.side_effect = ir_list
        client.get_SR.side_effect = sr_list
        utils.update_drivers_stats([member], client)

        assert_equal(client.get_irating.call_count, 4)
        assert_equal(client.get_SR.call_count, 4)

        assert_list_equal(sr_list, [member.oval_sr.licence_as_number, member.road_sr.licence_as_number,
                                    member.dOval_sr.licence_as_number, member.dRoad_sr.licence_as_number])

        assert_list_equal(ir_list, [member.oval_irating, member.road_irating,
                                    member.dOval_irating, member.dRoad_irating])

    @mock.patch("builtins.open", mock.mock_open(read_data=json.dumps({"drivers": [{"name": "John Doe", "id": 2020}]})))
    def test_parse_drivers(self):
            drivers = utils.parse_drivers("path")

            assert_equal(len(drivers), 1)
            assert_equal("John Doe", drivers[0].name)
            assert_equal(2020, drivers[0].custid)
