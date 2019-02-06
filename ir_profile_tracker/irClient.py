import json
import requests
from ir_profile_tracker.models import RaceType

LOGIN_GET = 'https://members.iracing.com/membersite/login.jsp'
LOGIN_POST = 'https://members.iracing.com/membersite/Login'
STATS_CHART = 'http://members.iracing.com/memberstats/member/GetChartData?custId={0}&catId={1}&chartType={2}'


class IrClient(object):
    """
    Class to perform queries to iRacing site.
    """
    def __init__(self):
        self.session = requests.session()
        self._logged = False

    def login(self, email, password):
        """
        Login using email/password.
        :param email: Email associated to your ir account
        :param password: Password of your account
        :return: True if logged
        :raise Exception if credentials are wrong or there is a connection problem.
        """
        if not self._logged:
            data = {'username': email, 'password': password,
                    'todaysdate': '', 'utcoffset': 300}

            if self.session.get(LOGIN_GET).status_code == 200:
                self.session.post(LOGIN_POST, data=data)

                if not self.session.cookies:
                    raise Exception("Iracing credentials are wrong")
                else:
                    print("Logged to iRacing site")
                    self._logged = True
            else:
                raise Exception("iRacing service unavalible.")

        return True

    def logout(self):
        self._logged = False
        del self.session.cookies

    def get_irating(self, memberid, racetype=RaceType.Oval):
        """
        Gets irtaing from a member
        :param memberid: iracing customer id
        :param racetype: Licence
        :return: irating value; None if there was an error
        """
        try:
            RaceType(racetype)
        except ValueError as VE:
            raise ValueError("Racetype is not valid") from VE

        url = STATS_CHART.format(memberid, racetype, 1)
        response = json.loads(self.session.get(url).text)

        try:
            return response[-1][1]
        except IndexError:
            return None

    def get_SR(self, memberid, racetype=RaceType.Oval):
        """
        Gets current SR from a member
        :param memberid: iRacing customer id
        :param racetype: Licence
        :return: SR as numeric value; None if there was an error
        """
        try:
            RaceType(racetype)
        except ValueError as VE:
            raise ValueError("Racetype is not valid") from VE

        url = STATS_CHART.format(memberid, racetype, 3)
        response = json.loads(self.session.get(url).text)

        try:
            return response[-1][1]
        except IndexError:
            return None

    def is_logged(self):
        return self._logged
