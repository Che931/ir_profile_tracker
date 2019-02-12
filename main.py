import argparse
import sys
import os
import settings
from ir_profile_tracker.irClient import IrClient
from ir_profile_tracker.utils import update_drivers_stats, drivers_to_csv, parse_drivers


def parse_args(args):
    parser = argparse.ArgumentParser(description='IR_Profile_Tracker')
    parser.add_argument('-f', '--file', help="Filename that contains driver's info'.", required=True)
    parser.add_argument('-o', '--output', help="Name of the output file(extension included).")

    return parser.parse_args(args)


def main(args):
    parser = parse_args(args)
    file = parser.file
    if os.path.exists(file):
        drivers = parse_drivers(file)

        client = IrClient()
        if client.login(settings.IRACING_EMAIL, settings.IRACING_PASSWORD):
            update_drivers_stats(drivers, client)
            drivers_to_csv(drivers, parser.output)
    else:
        raise FileNotFoundError("File {0} not found".format(parser.file))


if __name__ == "__main__":
    main(sys.argv[1:])
