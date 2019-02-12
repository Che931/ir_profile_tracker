from unittest import TestCase
from unittest import mock
from nose.tools import assert_equal, assert_raises, assert_true
from ir_profile_tracker.models import Member
import main


class TestArgumentParser(TestCase):

    def test_parse_file_arg(self):
        parse = main.parse_args(["-f", "file.json"])
        assert_equal(parse.file, "file.json")

    def test_parse_output_arg(self):
        parse = main.parse_args(["-f", "file.json", '--output', 'drivers.csv'])
        assert_equal(parse.output, "drivers.csv")

    def test_parse_zero_args_raise_exception(self):
        with assert_raises(SystemExit):
            main.parse_args([])


class TestMain(TestCase):

    def setUp(self):
        self.member = Member(name="John Doe", custid=2020)
        self.client_instance = mock.MagicMock()
        self.client_instance.login.return_value = True

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
    def test_main(self, mock_csv, mock_update_drivers, mock_client, mock_parse_drivers, mock_os):
        filename = 'file.json'
        mock_os.return_value = True
        mock_parse_drivers.return_value = [self.member]
        mock_client.return_value = self.client_instance

        main.main(["-f", filename])

        assert_true(mock_update_drivers.called)
        assert_true(self.client_instance.login.called)

        mock_parse_drivers.assert_called_once_with(filename)
        mock_update_drivers.assert_called_once_with([self.member], self.client_instance)
        mock_csv.assert_called_once_with([self.member], None)

    @mock.patch('main.os.path.exists')
    @mock.patch('main.parse_drivers')
    @mock.patch('main.IrClient')
    @mock.patch('main.update_drivers_stats')
    @mock.patch('main.drivers_to_csv')
    def test_main_custom_output_file(self, mock_csv, mock_update_drivers, mock_client, mock_parse_drivers, mock_os):
        filename = 'file.json'
        output = "stats.csv"

        mock_client.return_value = self.client_instance
        self.client_instance.login.return_value = True
        mock_os.return_value = True
        mock_parse_drivers.return_value = [self.member]

        main.main(["-f", filename, '-o', output])

        assert_true(mock_update_drivers.called)
        mock_csv.assert_called_once_with([self.member], output)
        mock_update_drivers.assert_called_once_with([self.member], self.client_instance)
