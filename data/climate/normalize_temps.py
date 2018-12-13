#!python3.6
"""
normalize_temps.py

Usage: python3 normalize_temps.py <list of .csv files>

Parses out .csv files from NOAA, removing unused columns and normalizing tempertures based on the
humidity and calculated distance from the DRY bulb temperature.

Outputs cleaned data to <same_file_name>_cleaned.csv
"""
import argparse
import csv
import logging
import sys
import time

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
INTERESTED_KEYS = [
    "STATION_NAME",
    "DATE",
    "HOURLYDRYBULBTEMPF",
    "HOURLYWETBULBTEMPF",
    "HOURLYRelativeHumidity",
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
        description="Normalize temperature scale against the humidity for the passed-in .csv file(s)."
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
        clean_rows = []
        this_csv_reader = csv.DictReader(dirty_csv)
        for row in this_csv_reader:
            cut_row = {}
            for key in INTERESTED_KEYS:
                cut_row[key] = row.get(key)
            try:
                temp_range = float(cut_row["HOURLYDRYBULBTEMPF"]) - float(cut_row["HOURLYWETBULBTEMPF"])
                temp_range_distance = float(
                    float(float(cut_row["HOURLYRelativeHumidity"]) / 100) * float(temp_range)
                )
                cut_row["NORMALIZED_TEMPERATURE"] = (
                    float(cut_row["HOURLYDRYBULBTEMPF"]) - temp_range_distance
                )
            except (IndexError, ValueError):
                continue
            clean_rows.append(cut_row)
        this_file_dur = time.time() - this_file_start
        logger.info(f"Processing this file took {this_file_dur:.2f} seconds.")
        logger.debug(f"CLEAN ROWS: {clean_rows[:10]}")
        clean_file_name = dirty_csv.name.split(".")[0] + "_normalized" + ".csv"
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
