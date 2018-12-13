#!python3.6
"""
aggregate_temps.py

Usage: python3 aggregate_temps.py <list of .csv files>

Aggregates weather data up from the hourly dimension to the weekly dimension, reporting weekly mean and standard deviation.

Outputs cleaned data to <same_file_name>_aggregated.csv
"""
from datetime import datetime
import argparse
import collections
import csv
import logging
import statistics
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "STATION_NAME",
    "YEAR",
    "WEEK OF YEAR",
    "MEAN",
    "STDDEV",
    "TEMPS"
]

def set_up_logger(verbose):
    try:
        log_level = LOG_LEVELS.pop(verbose)
    except IndexError:
        log_level = logging.DEBUG
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("[%(levelname)s]\t%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate data to the weekly level for the passed-in .csv file(s)."
    )
    parser.add_argument(
        "file", nargs="*", type=argparse.FileType("r"), help="The name(s) of a file to normalize."
    )
    parser.add_argument("-v", "--verbose", action="count", default=5)
    args = parser.parse_args()
    logger = set_up_logger(args.verbose)
    logger.debug(f"ARGS: {args}")
    for dirty_csv in args.file:
        this_file_start = time.time()
        logger.info(f"Working on {dirty_csv.name}.")
        date_to_hourly_times_mapping = collections.OrderedDict()
        this_csv_reader = csv.DictReader(dirty_csv)
        for row in this_csv_reader:
        	# 2014-08-02 06:51
            this_station = row["STATION_NAME"]
            this_date = row["DATE"]
            try:
                this_datetime = datetime.strptime(this_date, '%Y-%m-%d %H:%M')
            except ValueError: 
                # Probably did not match the format string; use the fallback
                # Notably the Ventura County data was of this format
                this_datetime = datetime.strptime(this_date, '%m/%d/%Y %H:%M')
            this_datetime_string = this_datetime.strftime("%Y #%U").strip()
            if this_datetime_string not in date_to_hourly_times_mapping:
            	date_to_hourly_times_mapping[this_datetime_string] = []
            date_to_hourly_times_mapping[this_datetime_string].append(float(row["NORMALIZED_TEMPERATURE"]))
        
        logger.info("Finished aggregating weekly temperature metrics!")
        logger.info("Now calculating weekly mean/standard deviations...")
        clean_rows = []
        for date_string, hourly_temps_list in date_to_hourly_times_mapping.items():
            day_average = statistics.mean(hourly_temps_list)
            day_stddev = statistics.pstdev(hourly_temps_list)
            this_year = date_string.split(" ")[0]
            this_week_num = date_string.split(" ")[1][1:]
            this_day_row = {    
                "STATION_NAME": this_station,
                "YEAR": this_year,
                "WEEK OF YEAR": this_week_num,
                "MEAN": "{0:.3f}".format(day_average),
                "STDDEV": "{0:.3f}".format(day_stddev),
                "TEMPS": str(hourly_temps_list)
            }
            clean_rows.append(this_day_row)

        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")

        clean_file_name = dirty_csv.name.replace("normalized", "aggregated")
        logger.info(f"Writing out to file named: {clean_file_name}!")
        with open(clean_file_name, "w", newline="") as cleanfile:
            this_writer = csv.DictWriter(cleanfile, fieldnames=INTERESTED_KEYS) 
            this_writer.writeheader()
            for row in clean_rows:
                this_writer.writerow(row)
        logger.info("Done writing file.")
        logger.info(f"Done processing file {dirty_csv.name}!")


if __name__ == "__main__":
    main()
