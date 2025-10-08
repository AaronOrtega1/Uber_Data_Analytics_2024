import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from lib.create_star_schema import StarSchemaCreator


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

    def create_staging_table(self, engine_connection):
        with engine_connection.connect() as conn:
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS staging_bookings (
                    booking_id              VARCHAR(50) PRIMARY KEY,
                    booking_status          VARCHAR(50),
                    customer_id             VARCHAR(50),
                    vehicle_type            VARCHAR(50),
                    pick_up_location        VARCHAR(200),
                    drop_location           VARCHAR(200),
                    avg_vtat                DECIMAL(5,2),
                    avg_ctat                DECIMAL(5,2),
                    cancelled_by_customer   BOOL,
                    customer_cancellation_reason VARCHAR(300),
                    cancelled_by_driver     BOOL,
                    driver_cancellation_reason VARCHAR(300),
                    incomplete_rides        BOOL,
                    incomplete_rides_reason TEXT,
                    booking_value           DECIMAL(10,2),
                    ride_distance           DECIMAL(6,2),
                    driver_rating           DECIMAL(2,1),
                    customer_rating         DECIMAL(2,1),
                    payment_method          VARCHAR(50),
                    booking_timestamp       TIMESTAMP
                )
            """
                )
            )
            conn.commit()


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

    df = etl.data

    # Load environment variables from the .env file
    load_dotenv()

    # Env variables
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    PORT = 5432
    HOST = "postgres"

    # DB engine
    conn_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}"
    engine = create_engine(conn_string)

    # Create staging table
    etl.create_staging_table(engine)

    # Change df columns names to all lowercase and change " " with "_"
    cols_names = [
        col_name.replace(" ", "_").lower() for col_name in df.columns.tolist()
    ]

    df.rename(columns=dict(zip(df.columns, cols_names)), inplace=True)

    # Remove duplicate booking_ids, keeping the first occurrence
    df = df.drop_duplicates(subset=["booking_id"], keep="first")

    # Load transformed data
    df.to_sql("staging_bookings", engine, if_exists="replace", index=False)
    print("ETL finished. Data transformed and loaded into staging_bookings")

    # Create and Populate star schema with StarSchemaCreator class.
    starSchema = StarSchemaCreator(engine)
    starSchema.create_star_schema()


if __name__ == "__main__":
    main()
