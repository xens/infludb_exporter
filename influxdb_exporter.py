#!/usr/bin/env python3

import argparse
import json
import datetime as dt
import requests

def get_metrics(host, db, measurement):
    """
    Get metrics from the InfluxDB server's API
    """
    url = "%s/query?pretty=true" % (host)
    payload = {'db': db,
               'chunk_size': '20000',
               'q': 'SELECT * FROM {0}'.format(measurement)}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    return data

def get_measurements(host):
    """
    Get list of all the different measurements inside a
    database.
    """
    url = "%s/query?pretty=true" % (host)
    payload = {'db': 'smartmetter_db',
               'chunk_size': '20000',
               'q': 'SHOW MEASUREMENTS'}
    r = requests.get(url, params=payload)
    measurements = sum(json.loads(r.text)["results"][0]["series"][0]["values"], [])
    return measurements

def time_format(rfc3339):
    """
    Reads the timestamp coded following
    RFC3339-micro format and convert it
    to EPOCH (millisecond)
    """
    rfc3339=rfc3339[:-4] # stripping micro-second informations
    try:
        epoch = dt.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%S.%f').timestamp()
        return epoch
    except ValueError:
        #print("Timestamp: %s is wrongly formated" % (rfc3339))
        return 1


def json_parser(data, measurement):
    """
    Extract the relevant information inside json values fields
    """
    count=0
    count_failed=0

    for i in range(len(data)):
        epoch=time_format(data[i][0])
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
    args = parser.parse_args()

    if args.host and args.db and args.file:
        measurements = get_measurements(args.host)
        file_out = open(args.file, 'w')
        raw_data={}
        for i in measurements:
            temp_data=(get_metrics(args.host, args.db, i))
            raw_data.update({i: temp_data})

        for key in raw_data:
          json_parser(raw_data[key]["results"][0]["series"][0]["values"], key)
        file_out.close()
    else:
        print("missing option, try -h (help)")


