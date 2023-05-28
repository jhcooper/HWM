from pandas import DataFrame
import pandas as pd


def filter_df(df: DataFrame, threshold: float, fileName: str):
    # Creates and saves a csv that contains only water level data from the provided site DataFrame that exceeds the
    # site's threshold. The csv is saved as 'filename_filtered.csv' in the 'Filtered_Data' folder.
    # Additionally, makes a call to filter_on_day to isolate HWM events that are separated by more than a day
    # Parameters:
    #   df: DataFrame - the csv file of the data, in pandas DF form
    #   threshold: float - the threshold for a HWM at the target station
    #   fileName: str - the location name and year (location_year)
    # Returns:
    #    df_isolated: DataFrame - the csv file of the data, in pandas DF form, now only containing isolated HWM events

    # Only include values greater than the threshold
    df_filtered = df[df['Water Level'] >= threshold]
    # Calculate time difference between consecutive rows
    df_filtered.to_csv(f"./Filtered_Data/{fileName}_filtered.csv", index=False)

    df_isolated = filter_on_day(df_filtered)
    return df_isolated


def filter_on_day(df: DataFrame):
    # Helper function to isolate HWM events from a pre-filtered DataFrame
    # Parameters:
    #   df: DataFrame - a filtered csv containing all threshold exceedances
    # Returns:
    #   isolated: DataFrame - contains only threshold exceedances that do not occur within the same 24-hour period

    # Create a time difference constant for same-day calculations
    time_diff = (df['Date Time'].diff().dt.total_seconds() / 3600)

    # Create a boolean series (true if not same day or null)
    isSameDay = (time_diff > 48) | pd.isnull(time_diff)

    # filter out all values that lie on the same day
    isolated = df[isSameDay];

    return isolated
