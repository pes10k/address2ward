#!/usr/bin/env python3
import argparse
import pathlib
import sys

import address2ward

PARSER = argparse.ArgumentParser(
    prog="address2ward",
    description="Returns best effort Chicago Aldermanic Ward for an address. "
                "Ward data is from https://data.cityofchicago.org/"
                "Facilities-Geographic-Boundaries/Boundaries-Wards-2023-Map/cdf7-bgn3.")
PARSER.add_argument(
    "address",
    help="Address to geolocate.")
PARSER.add_argument(
    "--cachedir",
    default="/tmp",
    type=pathlib.Path,
    help="Directory to read / write cached values to.")
ARGS = PARSER.parse_args()

WARD_ID = address2ward.ward_for_address(ARGS.address, ARGS.cachedir)
if WARD_ID:
    print(WARD_ID)
    sys.exit(0)

print(f"Unable to find ward for {ARGS.address}", file=sys.stderr)
sys.exit(1)
