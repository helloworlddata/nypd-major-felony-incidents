import argparse
from csv import DictReader, DictWriter
from datetime import datetime
from loggy import loggy
import re
from sys import stdout

LOGGY = loggy('clean')


RAW_HEADERS = [ "OBJECTID","Identifier","Occurrence Date","Day of Week",
                "Occurrence Month","Occurrence Day","Occurrence Year",
                "Occurrence Hour","CompStat Month","CompStat Day","CompStat Year",
                "Offense","Offense Classification","Sector","Precinct","Borough",
                "Jurisdiction","XCoordinate","YCoordinate","Location 1"]

CLEAN_HEADERS = ['occurrence_date', 'offense','borough', 'precinct',
                'latitude', 'longitude', 'sector',  'jurisdiction',
                 'compstat_date', 'object_id', 'identifier',
                  'xcoord', 'ycoord', ]

def clean_row(row):
    """
    returns a new dict
    """
    x = {}
    # fill in the boilerplate
    x['borough'] = row['Borough']
    x['identifier'] = row['Identifier']
    x['jurisdiction'] = row['Jurisdiction']
    x['object_id'] = row['OBJECTID']
    x['offense'] = row['Offense']
    x['precinct'] = row['Precinct']
    x['sector'] = row['Sector']
    x['xcoord'] = row['XCoordinate']
    x['ycoord'] = row['YCoordinate']

    # now fill in the derived values
    # some Occurrence Date values are blank
    try:
        dt = datetime.strptime(row['Occurrence Date'], '%m/%d/%Y %I:%M:%S %p')
        x['occurrence_date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as err:
        x['occurrence_date'] = None

    # Some Compstat values are blank
    # apparently compstat date is different than occurence date...
    try:
        x['compstat_date'] = datetime(int(row['CompStat Year']),
                                      int(row['CompStat Month']),
                                      int(row['CompStat Day']) ).strftime('%Y-%m-%row')
    except ValueError as err:
        x['compstat_date'] = None

    # Now try to split the Location 1 value into latitude/longitude
    _mtch = re.search(r'\((.+?), (.+?)\)', row['Location 1'])
    if _mtch:
        x['latitude'], x['longitude'] = _mtch.groups()
    else:
        x['latitude'] = x['longitude'] = None

    return x


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Clean data")
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    infile = args.infile

    csvin = DictReader(infile, fieldnames=RAW_HEADERS)
    csvout = DictWriter(stdout, fieldnames=CLEAN_HEADERS)
    csvout.writeheader()

    for row in csvin:
        if 'OBJECTID' in row.values():
            # ignore headers
            pass
        else:
            csvout.writerow(clean_row(row))

