# InfluxDB exporter

Download records from the InfluxDB API and write the output to a file
following the line-protocol specifications: https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_reference/

# Features

* Can extract all the measurements from a database

# Usage

```
usage: influxdb_exporter.py [-h] --host HOST --db DB --file FILE

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  hosts to connect to ex: http://192.168.1.1:8086
  --db DB      name of the DB to dump
  --file FILE  name of the file to write the data to
```

# Caveats

Really early-stage for now:

* loosing precsion on timestamps, converting from micro to miliseconds
