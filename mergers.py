import os
from pandas import DataFrame
import pandas as pd
from datetime import timedelta
from formatting import finalFormatting


def mergeOnDate(unfiltered: DataFrame, isolated: DataFrame, year: str):
    """
    Merges data from an unfiltered and isolated dataframe based on the date. Uses a scrolling time window to identify
    the unfiltered data's highest value for each two-day period surrounding each date in the isolated dataframe. The
    merged data is saved in the Yearly_Reports folder as {year}_Report.csv.

    Parameters:
        unfiltered (DataFrame): The unfiltered dataframe containing data for all sites and dates.
        isolated (DataFrame): The isolated dataframe containing data for isolated events.
        year (str): The year for which the data is being merged.

    Returns:
        None
    """
    result = pd.DataFrame(columns=isolated.columns)

    # Get a list of all site identifiers in the unfiltered dataframe
    all_sites = unfiltered['SiteID'].unique()

    # Loop through each row in the filtered dataframe
    for index, row in isolated.iterrows():
        # Extract the site identifier and date
        date = row['Date Time']

        # Find the two-day period around the filtered date
        start_date = date - timedelta(days=2)
        end_date = date + timedelta(days=2)

        # Filter the unfiltered dataframe to include only the rows for this date range
        date_range_data = unfiltered[(unfiltered['Date Time'] >= start_date) & (unfiltered['Date Time'] <= end_date)]

        # Loop through each site in the unfiltered dataframe
        for site in all_sites:
            # Filter the data to include only the rows for this other site
            other_site_data = date_range_data[date_range_data['SiteID'] == site]

            # If there are any rows for this other site, find the max water level
            if not other_site_data.empty:
                max_water_level_row = other_site_data.loc[other_site_data['Water Level'].idxmax()]
                # Add the result to the result dataframe
                result = result.append(max_water_level_row)
    result.drop_duplicates(subset=['Identifier'], inplace=True)
    result = result.iloc[:, 1:]
    result = result.sort_values(by='Date Time', ascending=True)
    result.reset_index(drop=True, inplace=True)

    result = finalFormatting(result)
    result.to_csv(f"./Yearly_Reports/{year}_Report.csv")


def mergeUnfiltered(year: str):
    """
      Merges all the unfiltered data for every site for a single year into a single csv. The
      merged data is saved in the Merged_Data/{year} folder as Unfiltered_Merged_{year}.csv

      Parameters:
          year (str): the year of the desired data

      Returns:
          None
      """
    folder_path = f"./Unfiltered_Data/{year}"

    # Create A list of All Unfiltered CSVS
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Open and Add All csvs
    data_frames = []
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Merge into a single DataFrame
    merged_df = pd.concat(data_frames, ignore_index=True)

    # Revert the 'Date', 'Time', and 'Date Time' columns to Date Time format
    merged_df['Date'] = pd.to_datetime(merged_df['Date'])
    merged_df['Date Time'] = pd.to_datetime(merged_df['Date Time'])
    merged_df['Time'] = pd.to_datetime(merged_df['Time'])

    # Create a yearly folder if needed
    folder_path = f"./Merged_Data/{year}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the merged data
    merged_df.to_csv(f"./Merged_Data/{year}/Unfiltered_Merged_{year}.csv")

    return merged_df


def mergeEvents(year: str):
    """
      Merges all the isolated data for Lewes, Bowers, and Reedy Point for a single year into a single csv. The
      merged data is saved in the Merged_Data/{year} folder as Isolated_Events_Merged_{year}.csv

      Parameters:
          year (str): the year of the desired data

      Returns:
          None
      """
    folder_path = f"./Isolated_Events/{year}"

    # Create A list of All Unfiltered CSVS
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Open and Add All csvs
    data_frames = []
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Merge into a single DataFrame
    merged_df = pd.concat(data_frames, ignore_index=True)

    merged_df['Date'] = pd.to_datetime(merged_df['Date'])
    merged_df['Date Time'] = pd.to_datetime(merged_df['Date Time'])
    merged_df['Time'] = pd.to_datetime(merged_df['Time'])

    file_path = f"./Merged_Data/{year}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    merged_df.to_csv(f"./Merged_Data/{year}/Isolated_Events_Merged_{year}.csv")

    return merged_df
