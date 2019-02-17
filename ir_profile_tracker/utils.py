import csv
import json
import time
from datetime import datetime
from ir_profile_tracker.models import RaceType, Member


def update_drivers_stats(drivers, irClient, ignore_licences=[]):
    """
    Updates drivers'info(irating and SR).
    :param drivers: Array that contains all memebers. See models.Member.
    :param irClient: irClient instance
    :param ignore_licences
    """
    licences = [rt for rt in RaceType if rt.value not in ignore_licences]
    for driver in drivers:
        print("Getting iR/SR from driver {0}".format(driver))
        for rt in licences:
            irating = irClient.get_irating(driver.custid, rt.value)
            time.sleep(.5)
            sr = irClient.get_SR(driver.custid, rt.value)

            driver.update_irating(rt, irating)
            driver.update_sr(rt, sr)


def drivers_to_csv(drivers, filename=None, ignore_licences=[]):
    """
    Exports drivers stats to a csv file
    :param drivers: Array with all members
    :param filename: output file extension included
    :param ignore_licences
    """
    output_file = filename if filename else 'driversStats.csv'
    ir_headers = ["ir_{0}".format(rt.name) for rt in RaceType if rt.value not in ignore_licences]
    sr_headers = ["sr_{0}".format(rt.name) for rt in RaceType if rt.value not in ignore_licences]

    with open(output_file, 'w') as file:
        csvfile = csv.writer(file, delimiter=',')
        csvfile.writerow(['Name', 'Id'] + ir_headers + sr_headers + ['Profile'])

        for driver in drivers:
            ir_dict = driver.irating_as_dict()
            sr_dict = driver.sr_as_dict()
            ir_info = [ir_dict[key] for key in ir_dict.keys() if key.value not in ignore_licences]
            sr_info = [str(sr_dict[key]) for key in sr_dict.keys() if key.value not in ignore_licences]

            csvfile.writerow([driver.name, driver.custid] + ir_info + sr_info + [driver.profile_url])

        ts = datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S UTC")
        csvfile.writerow([])
        csvfile.writerow(["Created: " + ts])
        print("File {0} created".format(output_file))


def parse_drivers(filepath):
    """
    Converts driver info from json to Member; see models.Member
    :param filepath: Path where json file is
    :return: Array with all members from json file; Empy array if file is empty
    """
    with open(filepath) as data:
        drivers = json.load(data)

        members = []
        for item in drivers['drivers']:
            member = Member(custid=item['id'], name=item['name'])
            members.append(member)
            print("Member {0} parsed".format(member))

    return members
