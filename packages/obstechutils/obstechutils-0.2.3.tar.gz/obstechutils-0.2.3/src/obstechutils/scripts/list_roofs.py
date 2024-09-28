#! /usr/bin/env python3

from obstechutils.roof import RoofInfo

from astropy.table import Table
import argparse

def main():

    parser = argparse.ArgumentParser(description='List all roofs and domes')
    parser.parse_args()

    roofs = RoofInfo.all_from_db()

    names = list(roofs[0].__dataclass_fields__.keys())

    rows = [tuple(getattr(roof, p) for p in names) for roof in roofs]

    tab = Table(rows=rows, names=names)
    tab.pprint_all()

if __name__ == "__main__":
    main()
