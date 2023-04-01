# lewes_file: str = '/Users/jh/Documents/HWM_Data/HWM_Lewes_05_2016.csv'
# reedy_file: str = '/Users/jh/Documents/HWM_Data/HWM_ReedyPoint_05_2016.csv'
from pandas import DataFrame
import pandas as pd
import requests
import io
from automated_retrieval import retrieve_NOAA
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

bowers_url: str = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no=01484085&period=&begin_date=2016-05-01&end_date=2017-05-01'
lewes_threshold = 4.37
bowers_threshold = 4.50
reedy_threshold = 4.53


def filter_on_day(df):
    time_diff = (df['Date Time'].diff().dt.total_seconds() / 3600)
    # Create a boolean series (true if not same day or null)
    isSameDay = (time_diff > 24) | pd.isnull(time_diff)
    # filter out all values that lie on the same day
    filtered = df[isSameDay];
    return filtered


def localize(df):
    # Convert to datetime format
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    # Set local timezone to UTC
    df['Date Time'] = df['Date Time'].dt.tz_localize('UTC')
    # Convert timezone to EST
    df['Date Time'] = df['Date Time'].dt.tz_convert('US/Eastern')


def getData(stationID, begin_date, end_date, source, product):
    if source == 'USGS':
        url = \
            f'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no={stationID}&period=&begin_date={begin_date[0:3]}-{begin_date[4:5]}-{begin_date[6:7]}&end_date={end_date[0:3]}-{end_date[4:5]}-{end_date[6:7]}'
        raw = requests.get(bowers_url)
        # Skip the header rows and parse the data using pandas
        df = pd.read_csv(io.StringIO(raw.content.decode('utf-8')), skiprows=26, delimiter='\t')
        # Remove extraneous row
        df = df.drop(0)
        # # Rename Water Level and Date Time Columns
        # df.rename(columns={'69431_00065': 'Peak Water Level', 'datetime': 'Date Time'}, inplace=True)
        # # Convert Water Levels from string to number
        # df['Peak Water Level'] = pd.to_numeric(df['Peak Water Level'], errors='coerce')
    else:
        df = retrieve_NOAA(begin_date, end_date, stationID, product)
    return df


def formatAndSave(df: DataFrame, source: str, fileName: str):
    if source == 'USGS':
        df.rename(columns={'69431_00065': 'Water Level', 'datetime': 'Date Time'}, inplace=True)
        # Convert Water Levels from string to number
        df['Water Level'] = pd.to_numeric(df['Water Level'], errors='coerce')
        df.drop(columns={'agency_cd', 'site_no', 'tz_cd'})
        df.index = pd.RangeIndex(start=0, stop=len(df))
        localize(df)
    else:
        # Fill missing High-High values and dates with High counterparts
        df['date_time_HH'].fillna(df['date_time_H'], inplace=True)
        df['HH_water_level'].fillna(df['H_water_level'], inplace=True)

        # Remove unneeded columns and Rename Water level and DateTime Columns
        df.rename(columns={'date_time_HH': 'Date Time', 'HH_water_level': 'Water Level'}, inplace=True)
        df.drop(
            columns={'date_time_H', 'H_water_level', 'date_time_L', 'L_water_level', 'date_time_LL',
                     'LL_water_level', },
            inplace=True)

        # Revert from DateTime indexing to linear Indexing
        df.index = pd.RangeIndex(start=0, stop=len(df))
        localize(df)
    df.to_csv(f"./Unfiltered_Data/{fileName}_Unfiltered.csv", index=False)
    return df


# def format_NOAA(df: DataFrame):
#
#     df.drop(['date_time_H', 'H_water_level', 'date_time_L', 'L_water_level', 'date_time_LL', 'LL_water_level'], axis=1,
#             inplace=True)
#
def graph(df, fileName, source, threshold):
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

    return df


def createReport(begin_date, end_date, stationID, source, fileName, threshold, product):
    # Predefine File Paths
    unfiltered_path = f'./Unfiltered_Data/{fileName}_unfiltered.csv'
    isolated_events_path = f'./Isolated_Events/{fileName}_unfiltered.csv'

    # Retrieve, Convert, Rename, and Reformat Data
    df = getData(stationID, begin_date, end_date, source, product)

    df = graph(df, fileName, source, threshold)

    # Filter Data, Creating and saving 'Filtered' and 'Isolated_Events'csv
    filtered = filter_df(df, threshold, fileName, source)
    filtered.to_csv(isolated_events_path)


def filter_df(df, threshold: float, fileName: str, source: str):
    # Only include values greater than the threshold
    df_filtered = df[df['Water Level'] >= threshold]
    # Calculate time difference between consecutive rows
    df_filtered.to_csv(f"./Filtered_Data/{fileName}_filtered.csv", index=False)
    return filter_on_day(df_filtered)


if __name__ == '__main__':
    createReport('20160101', '20161231', '8557380', 'NOAA', 'Lewes_2016', lewes_threshold, 'high_low')
    createReport('20160101', '20161231', '01484085', 'USGS', 'Bowers_2016', bowers_threshold, '')
