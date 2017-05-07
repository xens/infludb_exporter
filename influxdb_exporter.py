#!/usr/bin/env python3

import json
import datetime as dt
import requests

def get_metrics():
    """
    Get metrics from the InfluxDB server's API
    """
    url = "http://server:8086/query?pretty=true"
    payload = {'db': 'database',
               'chunk_size': '20000',
               'q': 'SELECT * FROM \"metric\"'}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    return data


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
      print("Timestamp: %s is wrongly formated" % (rfc3339))
      return 1


def json_parser(data):
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
        file_out.write("%s,host=%s value=%s %s\n" % (db_name, host, value, int(epoch)))
      else:
        count_failed=count_failed+1
        continue

    file_out.close()
    print("entries parsed: %s, failed: %s" % (count, count_failed))

raw_data = get_metrics()
db_name = raw_data["results"][0]["series"][0]["name"]
file_out = open('output_lineformat', 'w')
json_parser(raw_data["results"][0]["series"][0]["values"])
