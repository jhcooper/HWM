import os

from pandas import DataFrame
import pandas as pd
import requests
import io
from automated_retrieval import retrieve_NOAA
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

bowers_url: str = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no=01484085&period=&begin_date=2016-05-01&end_date=2017-05-01'
lewes_threshold = 4.37
bowers_threshold = 4.50
reedy_threshold = 4.53


def createReport(begin_date: str, end_date: str, stationID: str, source: str, fileName: str, threshold: float,
                 product: str = ""):
    # Master function to create and save Unfiltered, Filtered, and Isolated Events csvs as well as a png plot of threshold
    # exceedance for USGS or NOAA Water Level data
    # Parameters:
    #   begin_date: str - the beginning date of the desired data range (YYYYMMDD)
    #   end_date: str - the ending date of the desired data range (YYYYMMDD)
    #   stationID: str - the station ID of the desired station
    #   source: str - the data source (USGS or NOAA)
    #   fileName: str - the location name and year (location_year)
    #   threshold: float - the threshold for a HWM at the target station
    #   product: str - *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)
    # No Returns

    # Predefine Isolated File Path
    isolated_events_path = f'./Isolated_Events/{fileName}_Events.csv'

    # Retrieve, Convert, Rename, and Reformat Data
    df = getData(stationID, begin_date, end_date, source, product)

    df = graph(df, fileName, source, threshold)

    # Filter Data, Creating and saving 'Filtered' and 'Isolated_Events'csv
    filtered = filter_df(df, threshold, fileName)
    filtered.to_csv(isolated_events_path)


def getData(stationID: str, begin_date: str, end_date: str, source: str, product: str):
    # Function to handle data retrieval from USGS or NOAA
    # Parameters:
    #   begin_date: str - the beginning date of the desired data range (YYYYMMDD)
    #   end_date: str - the ending date of the desired data range (YYYYMMDD)
    #   stationID: str - the station ID of the desired station
    #   source: str - the data source (USGS or NOAA)
    #   product: str - *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)
    # Returns:
    #    df: DataFrame - the csv file of the data, in pandas DF form

    # If the data is coming from USGS:
    if source == 'USGS':
        # Retrieve the raw data
        url = \
            f'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no={stationID}&period=&begin_date={begin_date[0:4]}-{begin_date[4:6]}-{begin_date[6:]}&end_date={end_date[0:4]}-{end_date[4:6]}-{end_date[6:]}'
        raw = requests.get(url)
        print(url)
        # Skip the header rows and parse the data using pandas
        df = pd.read_csv(io.StringIO(raw.content.decode('utf-8')), comment='#', delimiter='\t')
        print(df)
        print(df.columns)
        # create a boolean mask for rows where agency_cd is not equal to "USGS"
        mask = df['agency_cd'] != "USGS"
        # drop the rows where the mask is True
        df.drop(index=df[mask].index, inplace=True)
        # Rename Columns to be Universal
        df.rename(columns={"site_no": "SiteID", "agency_cd": "Source"}, inplace=True)
        # Separate date and time
        df[['Date', 'Time']] = df['datetime'].str.split(' ', expand=True)
    # If the data is coming from NOAA
    else:
        # Retrieve the raw data
        df = retrieve_NOAA(begin_date, end_date, stationID, product)

        # Add Site ID and Source columns
        df["SiteID"] = stationID
        df["Source"] = source
    return df


def formatAndSave(df: DataFrame, source: str, fileName: str):
    # Helper function to universalize formatting and column naming for USGS and NOAA data, as well as localize timezone
    # to EDT. Creates and saves 'filename_Unfiltered.csv' in 'Unfiltered_Data' folder, which holds all from the given
    # station and date range properly formatted but unfiltered
    # Parameters:
    #   df: DataFrame - the csv file of the data, in pandas DF form
    #   source: str - the data source (USGS or NOAA)
    #   fileName: str - the location name and year (location_year)
    # Returns:
    #    df: DataFrame - the csv file of the data, in pandas DF form, now universally formatted and localized

    # If the data is coming from USGS:
    if source == 'USGS':

        # Rename Water level and DateTime Columns
        df.rename(columns={'69431_00065': 'Water Level', 'datetime': 'Date Time'}, inplace=True)

        # Convert Water Levels from string to number
        df['Water Level'] = pd.to_numeric(df['Water Level'], errors='coerce')

        # Remove unneeded columns
        df.drop(columns={'tz_cd', '69431_00065_cd'}, inplace=True)

        # Revert indexing from DateTime to linear numeric (0,1,2,3,...)
        df.index = pd.RangeIndex(start=0, stop=len(df))
        # Perform timezone conversion to EDT
        localize(df)

        df['Identifier'] = df["SiteID"] + "-" + fileName[-4:] + "-" + df.reset_index().index.astype(str)
    else:

        # Fill missing High-High values and dates with High counterparts
        df['date_time_HH'].fillna(df['date_time_H'], inplace=True)
        df['HH_water_level'].fillna(df['H_water_level'], inplace=True)

        # Rename Water level and DateTime Columns
        df.rename(columns={'date_time_HH': 'Date Time', 'HH_water_level': 'Water Level'}, inplace=True)

        # Remove unneeded columns
        df.drop(
            columns={'date_time_H', 'H_water_level', 'date_time_L', 'L_water_level', 'date_time_LL',
                     'LL_water_level', },
            inplace=True)
        # Revert indexing from DateTime to linear numeric (0,1,2,3,...)
        df.index = pd.RangeIndex(start=0, stop=len(df))

        # Perform timezone conversion to EDT
        localize(df)
        # Separate Date and Time
        df['Date'] = df['Date Time'].dt.date
        df['Time'] = df['Date Time'].dt.time

        df['Identifier'] = df["SiteID"] + "-" + fileName[-4:] + "-" + df.reset_index().index.astype(str)
    df.to_csv(f"./Unfiltered_Data/{fileName}_Unfiltered.csv", index=False)
    return df


def graph(df: DataFrame, fileName: str, source: str, threshold: float):
    # Generates a plot representation of water level at a site over a period of time compared to that site's threshold.
    # The generated plot is saved under 'filename_plot.png' in the 'Plots' Folder
    # Also makes a call to formatAndSave to first format the data and save the unfiltered data before manipulation.
    # Parameters:
    #   df: DataFrame - the csv file of the data, in pandas DF form
    #   source: str - the data source (USGS or NOAA)
    #   threshold: float - the threshold for a HWM at the target station
    # Returns:
    #    df: DataFrame - the csv file of the data, in pandas DF form, now universally formatted and localized

    # Format and Save the data as a csv
    df = formatAndSave(df, source, fileName)

    # Isolate DateTime as 'date' and corresponding water level as 'WL'
    date = df["Date Time"]
    value = df["Water Level"]

    # Create Plot Object
    fig, ax = plt.subplots(figsize=(8, 6))

    # Locator for Major Axis
    half_year_locator = mdates.MonthLocator(interval=1)
    ax.xaxis.set_major_locator(half_year_locator)

    # Formatter for Major Axis (Four Digit Year, Two Digit Month)
    year_month_formatter = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(year_month_formatter)

    # Plot Data
    ax.plot(date, value)

    # Isolate Data Location as 'location' and Year as 'year' from filename
    location = fileName[:-5]
    year = fileName[-4:]

    # Set Title and Axis Labels
    ax.set_title(f'{location} High/Low Tides {year}')
    ax.set_ylabel('Water Level')
    ax.set_xlabel('Date')

    # Add Threshold Line
    plt.axhline(y=threshold, color='r', linestyle='-')

    # Add Legend
    ax.legend(loc='lower left', title='Key', labels=['Water Level', 'Threshold'])

    # Formats X Labels
    fig.autofmt_xdate()

    # Export Final Graph as a png
    plt.savefig(f"./Plots/{fileName}_Plot.png")
    plt.close()
    return df


def filter_df(df, threshold: float, fileName: str):
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


def filter_on_day(df):
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


def localize(df):
    # Helper function to convert water level data from UTC to local timezone (EDT)
    # Parameters:
    #   df: DataFrame - a formatted DF containing water level or high low data
    # No Returns

    # Convert to datetime format
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    # Set local timezone to UTC
    df['Date Time'] = df['Date Time'].dt.tz_localize('UTC')
    # Convert timezone to EST
    df['Date Time'] = df['Date Time'].dt.tz_convert('US/Eastern')


def mergeOnDate(unfiltered: DataFrame, isolated: DataFrame):
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
    result.to_csv("Merged.csv")


def mergeUnfiltered():
    folder_path = "./Unfiltered_Data"

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

    merged_df.to_csv("./Merged_Data/Unfiltered_Merged.csv")

    return merged_df


def mergeEvents():
    folder_path = "./Isolated_Events"

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

    merged_df.to_csv("./Merged_Data/Events.csv")

    return merged_df


if __name__ == '__main__':
    for year in range(2016, 2023):
        start_date = str(year) + '0101'
        end_date = str(year) + '1231'
        print(year)
        # Lewes
        print("Lewes")
        createReport(start_date, end_date, '8557380', 'NOAA', 'Lewes_' + str(year), lewes_threshold, 'high_low')

        # Reedy
        print("Reedy")
        createReport(start_date, end_date, '8551910', 'NOAA', 'Reedy_' + str(year), reedy_threshold, 'high_low')

        # Bowers
        print("Bowers")
        createReport(start_date, end_date, '01484085', 'USGS', 'Bowers_' + str(year), bowers_threshold)

    unfiltered = mergeUnfiltered()
    isolated = mergeEvents()
    mergeOnDate(unfiltered, isolated)
