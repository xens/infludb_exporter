# InfluXtractor

Download records from the InfluxDB API and write the output to a file
following the line-protocol specifications: https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_reference/

# Features

* Can extract all the measurements from a database

# Exporting data

```
usage: influxtractor.py [-h] --host HOST --db DB --file FILE
                            [--timezone TIMEZONE]

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          hosts to connect to ex: http://192.168.1.1:8086
  --db DB              name of the DB to dump
  --file FILE          name of the file to write the data to
  --timezone TIMEZONE  timezone to convert the records to: ex +2 for GMT+2
```

# Importing data

Curl can be used to upload the extracted data.

```curl -XPOST --data-binary @file_in 'http://server/write?db=my_db&precision=ms'```

If you get ```{"error":"timeout"}``` when sending very large file, you'll
have to cut your file into smaller blocks.
