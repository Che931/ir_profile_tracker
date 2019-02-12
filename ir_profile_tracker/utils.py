import csv
import json
import time
from datetime import datetime
from ir_profile_tracker.models import RaceType, Member


def update_drivers_stats(drivers, irClient):
    """
    Updates drivers'info(irating and SR).
    :param drivers: Array that contains all memebers. See models.Member.
    :param irClient: irClient instance
    """
    for driver in drivers:
        print("Getting iR/SR from driver {0}".format(driver))
        for rt in RaceType:
            irating = irClient.get_irating(driver.custid, rt.value)
            time.sleep(.5)
            sr = irClient.get_SR(driver.custid, rt.value)

            driver.update_irating(rt, irating)
            driver.update_sr(rt, sr)


def drivers_to_csv(drivers, filename=None):
    """
    Exports drivers stats to a csv file
    :param drivers: Array with all members
    :param filename: outputfile extension included
    """
    output_file = filename if filename else 'driversStats.csv'
    with open(output_file, 'w') as file:
        csvfile = csv.writer(file, delimiter=',')

        csvfile.writerow(['Name', 'Id', 'ir-Road', 'ir-Oval', 'ir-DRoad', 'ir-DOval', 'sr-Road', 'sr-Oval',
                         'sr-DRoad', 'sr-DOval', 'Profile'])

        for driver in drivers:
            csvfile.writerow([driver.name, driver.custid, driver.road_irating, driver.oval_irating,
                              driver.dRoad_irating, driver.dOval_irating, driver.road_sr, driver.oval_sr,
                              driver.dRoad_sr, driver.dOval_sr, driver.profile_url])

        ts = datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S UTC")
        csvfile.writerow(['' for item in range(0, 9)])
        csvfile.writerow(["Created: " + ts])
        print("File {0} created".format(filename))


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
