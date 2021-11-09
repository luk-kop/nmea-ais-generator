# nmea-ais-generator

[![Python 3.8.5](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-385/)
[![pydantic](https://img.shields.io/badge/pydantic-1.8.2-blue.svg)](https://pydantic-docs.helpmanual.io/)
[![pyproj](https://img.shields.io/badge/pyproj-3.2.1-blue.svg)](https://pypi.org/project/pyproj/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

> The **nmea-ais-generator** is a simple [Automatic Identification System (AIS)](https://en.wikipedia.org/wiki/Automatic_identification_system) messages generator.
> This script can be useful for testing applications or systems that require some AIS raw data.

## Features
- The NMEA data generated by the script (**NMEA 0183** format) is sent to clients via UDP packets.
- Individual clients' data (IP address & UDP port) is loaded from the `clients.json` file. Max number of clients is 10.
- By default, the initial AIS tracks data is loaded from `tracks.json` file.
- Both clients and tracks data is validated during loading.
- The `AIVDM` **NMEA 0183** type sentences are supported. `AIVDM`- sentence received data from other vessels.
- Script generates following AIS messages:
  - Message type 1 - Position Report Class A;
  - Message type 5 - Static and Voyage Related Data.
- Scripts options:
  - the initial AIS data can be loaded from specified JSON file;
  - the generated NMEA output data can also be displayed on the CLI terminal;
  - the updated AIS data can be saved to a new JSON file on terminating of the script.
  
  
Terminal output example:
```bash
# AIS type 1 message
!AIVDM,1,1,,A,13q5W0PP1fQEpJVO9V>pIVgp0D7k,0*66
# AIS type 5 message
!AIVDM,2,1,1,A,53q5W0`00001=;O??20d4l62222222222222220T0000040HtNQi0CTjp888,0*0C
!AIVDM,2,2,1,A,88888888880,2*25
```

***
## Getting Started

Use the following instructions to run the script on your local machine.

### Requirements

Python third party packages:
* [pyproj](https://pypi.org/project/pyproj/)
* [pydantic](https://pydantic-docs.helpmanual.io/)
* [aenum](https://pypi.org/project/aenum/)

Before running the script, the following files should be properly updated:
* `clients.json` - the IP address (hostname) and port pair to which the UDP packet should be sent;
* `tracks.json` - object data that will be converted to NMEA format and then sent
> Example files can be found in the root directory of the project.

### Installation with venv
The script can be build and run locally with virtualenv tool. Run following commands in order to create virtual environment and install the required packages.
```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
### Running the script

Script usage:
```bash
(venv) $ python main.py -h
usage: main.py [-h] [-f FILENAME] [-s SAVE] [-o]

The NMEA AIS data generating script

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        JSON filename with initial AIS tracks data (default: tracks.json)
  -s SAVE, --save SAVE  JSON filename to which the updated AIS data should be saved when the script exits
  -o, --output          Display NMEA AIS data on the terminal screen
```

You can start the script using one of the following commands:
```bash
# Run script with default options - data loaded from "tracks.json" file
(venv) $ python main.py
# Run script and display generated NMEA AIS output data on the CLI terminal
(venv) $ python main.py -o
# Run script and save updated AIS data to 'updated-tracks.json' file
(venv) $ python main.py -s updated-tracks.json
# Run script and load initial data from 'updated-tracks.json' file
(venv) $ python main.py -f updated-tracks.json
```

***
## References
* [AIVDM/AIVDO protocol decoding](https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data)
* [AIS Standard](https://en.wikipedia.org/wiki/Automatic_identification_system)
* [Sample AIVDM messages](https://fossies.org/linux/gpsd/test/sample.aivdm)