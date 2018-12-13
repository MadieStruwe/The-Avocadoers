#!python3
"""
aggregate_temps.py

Usage: python3 aggregate_temps.py <list of .csv files>

Aggregates weather data up from the hourly dimension to the daily dimension, reporting daily mean and standard deviation.
Each day will be then assigned a score based on the data for that day.

Outputs cleaned data to <same_file_name>_aggregated.csv
"""
import argparse
import csv
import collections
from datetime import datetime
import logging
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "STATION_NAME",
    "DATE",
    "NORMALIZED_TEMPERATURE",
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
        description="Aggregate and assign daily scores for the passed-in .csv file(s)."
    )
    parser.add_argument(
        "file", nargs="*", type=argparse.FileType("r"), help="The name(s) of a file to normalize."
    )
    parser.add_argument("-v", "--verbose", action="count", default=3)
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
            this_date = row["DATE"]
            this_datetime = datetime.strptime(this_date, '%Y-%m-%d %H:%M')
            this_datetime_string = this_datetime.strftime("%Y-%m-%d").strip()
            if this_datetime_string not in date_to_hourly_times_mapping:
            	date_to_hourly_times_mapping[this_datetime_string] = []
            date_to_hourly_times_mapping[this_datetime_string].append(row["NORMALIZED_TEMPERATURE"])
            break
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
        logger.debug(f"CLEAN ROWS: {clean_rows[:10]}")

        continue
        clean_file_name = dirty_csv.name.split(".")[0] + "_aggregated" + ".csv"
        logger.info(f"Writing out to file named: {clean_file_name}!")
        with open(clean_file_name, "w", newline="") as cleanfile:
            this_writer = csv.DictWriter(cleanfile, fieldnames=INTERESTED_KEYS)  # CHANGE THIS
            this_writer.writeheader()
            for row in clean_rows:
                this_writer.writerow(row)
        logger.info("Done writing file.")
        logger.info(f"Done processing file {dirty_csv.name}!")


if __name__ == "__main__":
    main()
