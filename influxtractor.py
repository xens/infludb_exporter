#!/usr/bin/env python3

import argparse
import json
import requests

def get_metrics(host, db, measurement):
    """
    Get metrics from the InfluxDB server's API
    """
    url = "%s/query?pretty=true" % (host)
    payload = {'db': db,
               'chunk_size': '20000',
               'epoch': 'ms',
               'q': 'SELECT * FROM {0}'.format(measurement)}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    return data

def get_measurements(host, db):
    """
    Get list of all the different measurements inside a
    database.
    """
    url = "%s/query?pretty=true" % (host)
    payload = {'db': db,
               'chunk_size': '20000',
               'q': 'SHOW MEASUREMENTS'}
    r = requests.get(url, params=payload)
    measurements = sum(json.loads(r.text)["results"][0]["series"][0]["values"], [])
    return measurements


def json_parser(data, measurement, tz):
    """
    Extract the relevant information inside json values fields
    """
    count=0
    count_failed=0
    operator=tz[0]
    tz=int(tz[1:])*3600*1000

    for i in range(len(data)):
        if operator == "+":
            epoch=data[i][0]+tz
        else:
            epoch=data[i][0]-tz
        if epoch != 1:
          host=data[i][1]
          value=data[i][2]
          count=count+1
          file_out.write("%s,host=%s value=%s %s\n" % (measurement, host, value, int(epoch)))
        else:
          count_failed=count_failed+1
          continue

    print("measurement: %s, entries parsed: %s, failed: %s" % (measurement, count, count_failed))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help="hosts to connect to ex: http://192.168.1.1:8086")
    parser.add_argument('--db', required=True, help="name of the DB to dump")
    parser.add_argument('--file', required=True, help="name of the file to write the data to")
    parser.add_argument('--timezone', help="timezone to convert the records to: ex +2 for GMT+2")
    args = parser.parse_args()

    if args.timezone:
        tz = args.timezone

    else:
        tz="+0"

    if args.host and args.db and args.file:
        measurements = get_measurements(args.host, args.db)
        file_out = open(args.file, 'w')
        raw_data={}
        for i in measurements:
            temp_data=(get_metrics(args.host, args.db, i))
            raw_data.update({i: temp_data})

        for key in raw_data:
          json_parser(raw_data[key]["results"][0]["series"][0]["values"], key, tz)
        file_out.close()
    else:
        print("missing option, try -h (help)")
