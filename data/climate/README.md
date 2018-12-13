# climate

This directory holds the climate data & scripts.
Loose files in this directory are utility scripts, documented below.
Base data from NOAA is held in the `base` directory, temperature normalized data is held in `normalized`, and aggregated data is held in `aggregated`.

## normalize_temps.py

Author: Evan Lee (@Archetypically)

*Requires python >=3.6*

Cleans up data and normalizes temperature based on a calculated humidity scale.
Output data is written to same directory, using the pattern `<original_name>_normalized.csv`.

#### Usage

```bash
$ python3.6 normalize_temps.py -h
usage: normalize_temps.py [-h] [-v] [file [file ...]]

Normalize temperature scale against the humidity for the passed-in .csv
file(s).

positional arguments:
  file           The name(s) of a file to normalize.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

#### Output

```bash
$ python normalize_temps.py LosAngeles_LAX.csv SanBernadinoCounty_SanBernadinoInternational.csv SanDiegoCounty_SanDiegoInternationalAirport.csv SantaBarbara_SantaBarbaraMunicipal.csv VenturaCounty_CamarilloAirport.csv
[INFO]  Working on LosAngeles_LAX.csv.
[INFO]  Processing this file took 3.65 seconds.
[INFO]  Writing out to file named: LosAngeles_LAX_normalized.csv!
[INFO]  Done writing file.
[INFO]  Done processing file LosAngeles_LAX.csv!
[INFO]  Working on SanBernadinoCounty_SanBernadinoInternational.csv.
[INFO]  Processing this file took 1.08 seconds.
[INFO]  Writing out to file named: SanBernadinoCounty_SanBernadinoInternational_normalized.csv!
[INFO]  Done writing file.
[INFO]  Done processing file SanBernadinoCounty_SanBernadinoInternational.csv!
[INFO]  Working on SanDiegoCounty_SanDiegoInternationalAirport.csv.
[INFO]  Processing this file took 3.72 seconds.
[INFO]  Writing out to file named: SanDiegoCounty_SanDiegoInternationalAirport_normalized.csv!
[INFO]  Done writing file.
[INFO]  Done processing file SanDiegoCounty_SanDiegoInternationalAirport.csv!
[INFO]  Working on SantaBarbara_SantaBarbaraMunicipal.csv.
[INFO]  Processing this file took 3.31 seconds.
[INFO]  Writing out to file named: SantaBarbara_SantaBarbaraMunicipal_normalized.csv!
[INFO]  Done writing file.
[INFO]  Done processing file SantaBarbara_SantaBarbaraMunicipal.csv!
[INFO]  Working on VenturaCounty_CamarilloAirport.csv.
[INFO]  Processing this file took 3.39 seconds.
[INFO]  Writing out to file named: VenturaCounty_CamarilloAirport_normalized.csv!
[INFO]  Done writing file.
[INFO]  Done processing file VenturaCounty_CamarilloAirport.csv!
```

## aggregate_temps.py

Author: Evan Lee (@Archetypically)

*Requires python >=3.6*

Cleans up data and normalizes temperature based on a calculated humidity scale.
OAggregates weather data up from the hourly dimension to the daily dimension, reporting daily mean and standard deviation.
Each day will be then assigned a score based on the data for that day.

Assumes you are using the `*_normalized.csv` files from the output of `normalize_temps.py`.
Outputs cleaned data to `<same_file_name>_aggregated.csv`

#### Usage

```bash
$ python3.6 aggregate_temps.py -h
usage: aggregate_temps.py [-h] [-v] [file [file ...]]

Aggregate and assign daily scores for the passed-in .csv file(s).

positional arguments:
  file           The name(s) of a file to normalize.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

#### Output

```bash
$ python3.6 aggregate_temps.py normalized/VenturaCounty_CamarilloAirport_normalized.csv
[INFO]  Working on normalized/VenturaCounty_CamarilloAirport_normalized.csv.
[INFO]  Finished aggregating daily temperature metrics!
[INFO]  Now calculating daily mean/standard deviations...
[INFO]  Processing this file took 3.54 seconds.
[INFO]  Writing out to file named: aggregated/VenturaCounty_CamarilloAirport_aggregated.csv!
[INFO]  Done writing file.
[INFO]  Done processing file normalized/VenturaCounty_CamarilloAirport_normalized.csv!
```