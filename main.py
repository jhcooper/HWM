import pandas as pd
import numpy as np
from datetime import datetime
import requests
import io
import pytz as pz

lewes_threshold = 4.37
bowers_threshold = 4.50
reedy_threshold = 4.53


def convert_meters_to_feet(df):
    # Convert and round water levels to feet
    df[' Water Level'] = df[' Water Level'].apply(lambda x: round(x * 3.281, 3))

def filter_df(df, threshold: float, siteAndDate: str):
    # Only include values greater than the threshold
    df_filtered = df[df[' Water Level'] >= threshold]
    # Calculate time difference between consecutive rows
    df_filtered.to_csv(f"{siteAndDate}.csv",index = False)
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

def merge_data(df1,df2):
    df1['Date'] = df1['Date Time'].dt.date  # Separate date from Date Time column
    df1['Time'] = df1['Date Time'].dt.time  # Separate time from Date Time column

    df2['Date'] = df2['Date Time'].dt.date
    df2['Time'] = df2['Date Time'].dt.time

    merged_df = pd.merge(df1,df2,on ='Date',how = 'inner')  # Merges df1 and df2, including only days that are the same
    return merged_df

def prepare_data (filename, threshold):
    if filename[0:5] == 'https':
        raw = requests.get(bowers_url)
        # Skip the header rows and parse the data using pandas
        df = pd.read_csv(io.StringIO(raw.content.decode('utf-8')), skiprows=26, delimiter='\t')
        # Remove extraneous row
        df = df.drop(0)
        # Rename Water Level and Date Time Columns
        df.rename(columns={'69431_00065': ' Water Level', 'datetime': 'Date Time'}, inplace=True)
        # Convert Water Levels from string to number
        df[' Water Level'] = pd.to_numeric(df[' Water Level'], errors='coerce')
    else:
        df = pd.read_csv(filename)
        convert_meters_to_feet(df)
    df_formatted = reformat(df)
    return df_formatted

def locate_parallels (filtered_df , target_df):

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




if __name__ == '__main__':
    lewes_file: str = '/Users/jh/Documents/HWM_Data/HWM_Lewes_05_2016.csv'
    reedy_file: str = '/Users/jh/Documents/HWM_Data/HWM_ReedyPoint_05_2016.csv'
    bowers_url: str = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no=01484085&period=&begin_date=2016-05-01&end_date=2017-05-01'

    lewes_unfiltered = prepare_data(lewes_file, lewes_threshold)
    reedy_unfiltered = prepare_data(reedy_file, reedy_threshold)
    bowers_unfiltered = prepare_data(bowers_url, bowers_threshold)


    lewes_filtered = filter_df(lewes_unfiltered,lewes_threshold,'Lewes_June_2016')
    reedy_filtered = filter_df(reedy_unfiltered,reedy_threshold, 'Reedy_June_2016')
    bowers_filtered = filter_df(bowers_unfiltered,bowers_threshold, 'Bowers_June_2016')
