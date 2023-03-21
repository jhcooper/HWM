# lewes_file: str = '/Users/jh/Documents/HWM_Data/HWM_Lewes_05_2016.csv'
# reedy_file: str = '/Users/jh/Documents/HWM_Data/HWM_ReedyPoint_05_2016.csv'
bowers_url: str = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no=01484085&period=&begin_date=2016-05-01&end_date=2017-05-01'
import pandas as pd
import requests
import io
from automated_retrieval import retrieve_NOAA

lewes_threshold = 4.37
bowers_threshold = 4.50
reedy_threshold = 4.53


def convert_meters_to_feet(df):
    # Convert and round water levels to feet
    df['Water Level'] = df['Water Level'].apply(lambda x: round(x * 3.281, 3))


def filter_df(df, threshold: float, fileName: str):
    # Only include values greater than the threshold
    df_filtered = df[df['Water Level'] >= threshold]
    # Calculate time difference between consecutive rows
    df_filtered.to_csv(f"./Filtered_Data/{fileName}_filtered.csv", index=False)
    return filter_on_day(df_filtered)


def filter_on_day(df):
    time_diff = (df['Date Time'].diff().dt.total_seconds() / 3600)
    # Create a boolean series (true if not same day or null)
    isSameDay = (time_diff > 24) | pd.isnull(time_diff)
    # filter out all values that lie on the same day
    filtered = df[isSameDay];
    return filtered


def reformat(df):
    # Convert to datetime format
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    # Set local timezone to UTC
    df['Date Time'] = df['Date Time'].dt.tz_localize('UTC')
    # Convert timezone to EST
    df['Date Time'] = df['Date Time'].dt.tz_convert('US/Eastern')
    # Rename 'O or I (for verified)' column to 'Flag'
    df.rename(columns={' O or I (for verified)': 'Flag', }, inplace=True)
    return df


def getData(stationID, begin_date, end_date, source, product):
    if source == 'USGS':
        url = \
            f'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no={stationID}&period=&begin_date={begin_date[0:3]}-{begin_date[4:5]}-{begin_date[6:7]}&end_date={end_date[0:3]}-{end_date[4:5]}-{end_date[6:7]}'
        raw = requests.get(bowers_url)
        # Skip the header rows and parse the data using pandas
        df = pd.read_csv(io.StringIO(raw.content.decode('utf-8')), skiprows=26, delimiter='\t')
        # Remove extraneous row
        df = df.drop(0)
        # Rename Water Level and Date Time Columns
        df.rename(columns={'69431_00065': 'Water Level', 'datetime': 'Date Time'}, inplace=True)
        # Convert Water Levels from string to number
        df['Water Level'] = pd.to_numeric(df['Water Level'], errors='coerce')
    else:
        df = retrieve_NOAA(begin_date, end_date, stationID, product)
        format_NOAA(df)
        convert_meters_to_feet(df)
    df_formatted = reformat(df)
    return df_formatted


def locate_parallels(filtered_df, target_df):
    # Separate date and time for filtered_df
    filtered_df.loc[:, 'Date'] = filtered_df['Date Time'].dt.date
    filtered_df.loc[:, 'Time'] = filtered_df['Date Time'].dt.time
    # Separate date and time for target_df
    target_df.loc[:, 'Date'] = target_df['Date Time'].dt.date
    target_df.loc[:, 'Time'] = target_df['Date Time'].dt.time

    dates = filtered_df['Date']
    matched_dates = target_df[target_df['Date'].isin(dates)]
    print(matched_dates)

    time_diff = (matched_dates['Date Time'].diff().dt.total_seconds() / 3600)
    # Create a boolean series (true if not same day or null)
    isSameDay = (time_diff > 24) | pd.isnull(time_diff)
    # filter out all values that lie on the same day
    filtered = time_diff[isSameDay]
    return filtered


def format_NOAA(df):
    df['Date Time'] = df.index
    df.rename(columns={'water_level': 'Water Level'}, inplace=True)


def createReport(begin_date, end_date, stationID, source, fileName, threshold, product):
    df = getData(stationID, begin_date, end_date, source, product)
    unfiltered_path = f'./Unfiltered_Data/{fileName}_unfiltered.csv'
    df.to_csv(unfiltered_path)
    isolated_events_path = f'./Isolated_Events/{fileName}_unfiltered.csv'
    filtered = filter_df(df, threshold, fileName)
    filtered.to_csv(isolated_events_path)


if __name__ == '__main__':
    createReport('20160501', '20161231', '8557380', 'NOAA', 'Lewes_2016', lewes_threshold, 'water_level')
    createReport('20160501', '20161231', '01484085', 'USGS', 'Bowers_2016', bowers_threshold, '')
