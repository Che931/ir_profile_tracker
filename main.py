import argparse
import sys
import os
import settings
from ir_profile_tracker.irClient import IrClient
from ir_profile_tracker.models import RaceType
from ir_profile_tracker.utils import update_drivers_stats, drivers_to_csv, parse_drivers


class IgnoreLicenceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        choices = [item.value for item in RaceType]
        ignore_list = []
        for value in values:
            if value not in choices:
                raise argparse.ArgumentError(self, "Value {0} is not a valid licence".format(value))
            ignore_list.append(value)

        setattr(namespace, self.dest, ignore_list)


def parse_args(args):
    parser = argparse.ArgumentParser(description='IR_Profile_Tracker')
    parser.add_argument('-f', '--file', help="Filename that contains driver's info'.", required=True)
    parser.add_argument('-o', '--output', help="Name of the output file(extension included).")
    parser.add_argument('--ignore', action=IgnoreLicenceAction, nargs='*', type=int,
                        help="Licences that will not be exported (1-O, 2-R, 3-Dov, 4-Dr).")

    return parser.parse_args(args)


def main(args):
    parser = parse_args(args)
    file = parser.file
    ignore_list = parser.ignore

    if os.path.exists(file):
        drivers = parse_drivers(file)

        client = IrClient()
        if client.login(settings.IRACING_EMAIL, settings.IRACING_PASSWORD):
            update_drivers_stats(drivers, client, ignore_list)
            drivers_to_csv(drivers, parser.output, ignore_list)
    else:
        raise FileNotFoundError("File {0} not found".format(parser.file))


if __name__ == "__main__":
    main(sys.argv[1:])
