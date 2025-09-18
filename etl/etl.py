import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class ETL:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame.

        Args:
                data (pd.DataFrame): The DataFrame containing the data to process.
        """
        self.data = data

    def merge_date_time_to_timestamp(
        self, col_date: str, col_time: str, col_timestamp: str = "timestamp"
    ):
        """
        Converts a date column and a time column in the DataFrame to datetime objects in a new column.

        Args:
                col_date (str): Name of the date column.
                col_time (str): Name of the time column.
                col_timestamp (str): Desired name of the timestamp column. (Default: timestamp)
        """
        # Check if columns exist
        if col_date not in self.data.columns:
            raise KeyError(f"Column '{col_date}' not found in DataFrame")
        if col_time not in self.data.columns:
            raise KeyError(f"Column '{col_time}' not found in DataFrame")

        # Merge Date + Time into single timestamp
        self.data[col_timestamp] = pd.to_datetime(
            self.data[col_date] + " " + self.data[col_time]
        )

        return self.data


def main():
    input_path = "/data/ncr_ride_bookings.csv"

    # Read CSV
    df = pd.read_csv(input_path)

    # Initialize the etl class with the df as data
    etl = ETL(df)

    # Merge Date and Time cols into booking_timestamp col
    df = etl.merge_data_time_to_timestamp("Date", "Time", "booking_timestamp")


if __name__ == "__main__":
    main()
