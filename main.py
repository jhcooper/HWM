import pandas as pd
import numpy as np

def convert_Meters_to_Feet(df):
    df_converted = df
    df_converted[' Water Level'] = df_converted[' Water Level'].apply(lambda x: round(x*3.281,3))
    return df_converted
def filter_HWM(df, threshold):
    df_filtered = df[df[' Water Level'] > 4.37]
    return df_filtered
def reformat_df(df):
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    df['Date'] = df['Date Time'].dt.date
    df['Time'] = df['Date Time'].dt.time
    df.drop('Date Time', inplace=True, axis=1)
    df.rename(columns={' O or I (for verified)': 'Flag'}, inplace=True)
    df.reindex(columns=['Date', 'Time', ' Water Level', ' Sigma', 'flag', ' F', ' R', ' L', ' Quality '])
    return df


if __name__ == '__main__':
    filename: str = '/Users/jh/Documents/HWM_Data/HWM_Lewes_05_2016.csv'
    df = pd.read_csv(filename)
    print(df.columns)
    print(df.head())
    df = reformat_df(df)
    print(df.columns)
    print(df.head())
    df_converted = convert_Meters_to_Feet(df)
    print(df_converted.head())
    # df_filtered = filter_HWM(df)
    # print(df_filtered.head())
