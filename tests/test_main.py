from unittest import TestCase
from unittest import mock
import json
from datetime import datetime
from nose.tools import assert_equal, assert_raises, assert_list_equal, assert_true
from ir_profile_tracker.models import Member
import main


class TestMain(TestCase):

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

    @mock.patch('main.os.path.exists')
    def test_main_file_not_exists_raise_FileException(self, mock_os):
        mock_os.return_value = False
        with assert_raises(FileNotFoundError):
            main.main(["-f", "file.json"])

    @mock.patch('main.os.path.exists')
    @mock.patch('main.parse_drivers')
    @mock.patch('main.IrClient')
    @mock.patch('main.update_drivers_stats')
    @mock.patch('main.drivers_to_csv')
    def test_main(self, mock_csv, mock_up_drivers, mock_client, mock_p_drivers, mock_os):
        filename = 'file.json'
        member = Member(custid=2020, name="John")
        mock_os.return_value = True
        mock_p_drivers.return_value = [member]

        client_instance = mock.MagicMock()
        mock_client.return_value = client_instance
        client_instance.login.return_value = True

        main.main(["-f", filename])

        mock_p_drivers.assert_called_once_with(filename)
        assert_true(client_instance.login.called)
        assert_equal(mock_up_drivers.call_args[0][0][0], member)
        assert_true(mock_up_drivers.called)
        mock_csv.assert_called_once_with([member])

    @mock.patch('main.os.path.exists')
    @mock.patch('main.parse_drivers')
    @mock.patch('main.IrClient')
    @mock.patch('main.update_drivers_stats')
    @mock.patch('main.drivers_to_csv')
    def test_main_custom_output_file(self, mock_csv, mock_up_drivers, mock_client, mock_p_drivers, mock_os):
        filename = 'file.json'
        output = "stats.csv"

        member = Member(custid=2020, name="John")
        mock_os.return_value = True
        mock_p_drivers.return_value = [member]

        client_instance = mock.MagicMock()
        mock_client.return_value = client_instance
        client_instance.login.return_value = True

        main.main(["-f", filename, '-o', output])

        mock_csv.assert_called_once_with([member], output)

    def test_parse_file_arg(self):
        parse = main.parse_args(["-f", "file.json"])
        assert_equal(parse.file, "file.json")

    def test_parse_output_arg(self):
        parse = main.parse_args(["-f", "file.json", '--output', 'drivers.csv'])
        assert_equal(parse.output, "drivers.csv")

    def test_parse_zero_args_raise_exception(self):
        with assert_raises(SystemExit):
            main.parse_args([])

    @mock.patch("builtins.open")
    def test_drivers_to_csv_open_file(self, mock_open):
        main.drivers_to_csv([self.member])
        mock_open.assert_called_once_with("driversStats.csv", "w")

    @mock.patch("builtins.open")
    def test_drivers_to_csv_drivers_info(self, mock_open):
        main.drivers_to_csv([self.member])
        mock_open.assert_called_once_with("driversStats.csv", "w")
        assert_equal(mock_open().__enter__().write.call_count, 4)

        drivers_call_args = self.get_write_calls_arg(mock_open.mock_calls, 1)
        driver_expected_args = [self.member.name, self.member.custid, self.member.road_irating,
                                self.member.oval_irating, self.member.dRoad_irating, self.member.dOval_irating,
                                self.member.road_sr, self.member.oval_sr, self.member.dRoad_sr,
                                self.member.dOval_sr, self.member.profile_url]

        assert_list_equal(drivers_call_args, [str(item) for item in driver_expected_args])

    @mock.patch("builtins.open")
    @mock.patch("main.datetime")
    def test_drivers_to_csv_created_date(self, mock_dt, mock_open):
        today = datetime(2019, 2, 4, 1, 0, 0, 0)
        mock_dt.utcnow.return_value = today

        main.drivers_to_csv([self.member])
        date_call_args = self.get_write_calls_arg(mock_open.mock_calls, 3)

        assert_equal(date_call_args[0], "Created: " + today.strftime("%d-%b-%Y %H:%M:%S UTC"))
        assert_equal(mock_open().__enter__().write.call_count, 4)

    @mock.patch("builtins.open")
    def test_drivers_to_csv_file_headers(self, mock_open):
        main.drivers_to_csv([self.member])

        headers_call_args = self.get_write_calls_arg(mock_open.mock_calls, 0)
        headers_expected = ['Name', 'Id', 'ir-Road', 'ir-Oval', 'ir-DRoad', 'ir-DOval', 'sr-Road', 'sr-Oval',
                            'sr-DRoad', 'sr-DOval', 'Profile']

        assert_list_equal(headers_call_args, headers_expected)
        assert_equal(mock_open().__enter__().write.call_count, 4)

    @mock.patch("builtins.open", mock.mock_open(read_data=json.dumps({"drivers": [{"name": "John Doe", "id": 2020}]})))
    def test_parse_drivers(self):
            drivers = main.parse_drivers("path")

            assert_equal(len(drivers), 1)
            assert_equal("John Doe", drivers[0].name)
            assert_equal(2020, drivers[0].custid)

    @mock.patch('main.time.sleep', return_value=None)
    def test_update_drivers(self, mock_time):
        client = mock.Mock()
        ir_list = [1000, 1500, 3000, 2500]
        sr_list = [2342, 4365, 5499, 2128]

        client.get_irating.side_effect = ir_list
        client.get_SR.side_effect = sr_list

        main.update_drivers_stats([self.member], client)

        assert_equal(client.get_irating.call_count, 4)
        assert_equal(client.get_SR.call_count, 4)

        assert_list_equal(sr_list, [self.member.oval_sr.licence_as_number, self.member.road_sr.licence_as_number,
                                    self.member.dOval_sr.licence_as_number, self.member.dRoad_sr.licence_as_number])

        assert_list_equal(ir_list, [self.member.oval_irating, self.member.road_irating,
                                    self.member.dOval_irating, self.member.dRoad_irating])
