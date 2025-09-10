import pandas as pd


class ETL:
    def __init__(self, data):
        """
        Initialize the class with a DataFrame.

        Args:
                data (pd.DataFrame): The DataFrame containing the data to process.
        """
        self.data = data


def main():
    input_path = "/data/ncr_ride_bookings.csv"
    output_path = "/data/ncr_ride_bookings_transformed.csv"
    # Read CSV
    df = pd.read_csv(input_path)
    etl = ETL(df)
    # Write CSV
    df.to_csv(output_path, index=False)
    print(f"Saved transformed csv to {output_path}")


if __name__ == "__main__":
    main()
