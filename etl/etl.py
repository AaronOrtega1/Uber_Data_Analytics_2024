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

    def _delete_col(self, col_name: str):
        """
        Delete a column from a DataFrame
            Args:
                col_name (str) : Name of the colums to delete.
        """

        # Check if column exist
        if col_name not in self.data.columns:
            raise KeyError(f"Column '{col_name}' not found in DataFrame")

        self.data = self.data.drop(col_name, axis=1)

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

        # Drop date and time columns
        self._delete_col(col_date)
        self._delete_col(col_time)

    def remove_triple_quotes(self, col_name: str):
        """
        Remove triple quotes from a column in the DataFrame.

        Args:
                col_name (str): Name of the column which we want to remove triple quotes.
        """

        # Check if columns exist
        if col_name not in self.data.columns:
            raise KeyError(f"Column '{col_name}' not found in DataFrame")

        self.data[col_name] = self.data[col_name].str.replace('"', "").str.strip()

    def convert_cancelled_incomplete_into_bools(self, col_name):
        """
        Convert callled or incomplete flags into booleans for specific columns

        Args:
                col_name (str): Name of the column which we want to remove triple quotes.
        """

        # Check if columns exist
        if col_name not in self.data.columns:
            raise KeyError(f"Column '{col_name}' not found in DataFrame")

        self.data[col_name] = self.data[col_name].notna()


def main():
    input_path = "/data/ncr_ride_bookings.csv"

    # Read CSV
    df = pd.read_csv(input_path)

    # Initialize the etl class with the df as data
    etl = ETL(df)

    # Merge Date and Time cols into booking_timestamp col
    etl.merge_date_time_to_timestamp("Date", "Time", "booking_timestamp")

    # Remove triple quotes
    remove_triple_quotes_cols = ["Customer ID", "Booking ID"]

    for col in remove_triple_quotes_cols:
        etl.remove_triple_quotes(col)

    # Turn flags in cols to booleans
    cancelled_incomplete_cols = [
        "Cancelled Rides by Customer",
        "Cancelled Rides by Driver",
        "Incomplete Rides",
    ]

    for col in cancelled_incomplete_cols:
        etl.convert_cancelled_incomplete_into_bools(col)


if __name__ == "__main__":
    main()
