from pandas import DataFrame
import pandas as pd
import os


def formatAndSave(df: DataFrame, source: str, offset: float, datum: str, fileName: str, stationID: str, year: int,
                  product: str):
    """
    Helper function to universalize formatting and column naming for USGS and NOAA data, as well as localize timezone
    to EDT. Creates and saves 'filename_Unfiltered.csv' in 'Unfiltered_Data' folder, which holds all from the given
    station and date range properly formatted but unfiltered

    Parameters:
      df (DataFrame): the csv file of the data, in pandas DF form
      source (str): the data source (USGS or NOAA)
      fileName (str):  the location name and year (location_year)
      product (str): *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)

    Returns:
       df (DataFrame): the csv file of the data, in pandas DF form, now universally formatted and localized
    """
    # If the data is coming from USGS:
    folder_path = f"./Unfiltered_Data/{year}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if source == 'USGS':
        if not any(col.endswith('_00065') for col in df.columns):
            print("No Data Available")
            return
        # create a boolean mask for rows where agency_cd is not equal to "USGS"
        mask = df['agency_cd'] != "USGS"
        # drop the rows where the mask is True
        df.drop(index=df[mask].index, inplace=True)
        # Rename Columns to be Universal
        df.rename(columns={"site_no": "SiteID", "agency_cd": "Source"}, inplace=True)

        # Rename Water level and DateTime Columns
        df = df.rename(columns=lambda x: 'Water Level' if x.endswith('_00065') else x)
        df.rename(columns={'datetime': 'Date Time'}, inplace=True)

        # Convert Water Levels from string to number
        df['Water Level'] = pd.to_numeric(df['Water Level'], errors='coerce')

        # Remove unneeded columns
        df.drop(columns={'tz_cd'}, inplace=True)
        df = df.drop([col for col in df.columns if col.endswith('_00065_cd')], axis=1)

        # Perform timezone conversion to EDT
        handleTime(df)

    else:

        if product == "water_level":
            df['Date Time'] = df.index
            df.rename(columns={'water_level': 'Water Level'}, inplace=True)
        else:
            # Fill missing High-High values and dates with High counterparts
            df['date_time_HH'].fillna(df['date_time_H'].combine_first(df['date_time_L']), inplace=True)
            df['HH_water_level'].fillna(df['H_water_level'].combine_first(df['L_water_level']), inplace=True)

            # Rename Water level and DateTime Columns
            df.rename(columns={'date_time_HH': 'Date Time', 'HH_water_level': 'Water Level'}, inplace=True)

            # Remove unneeded columns
            df.drop(
                columns={'date_time_H', 'H_water_level', 'date_time_L', 'L_water_level', 'date_time_LL',
                         'LL_water_level', },
                inplace=True)
        # Add Site ID and Source columns
        df["SiteID"] = stationID
        df["Source"] = source
        # Revert indexing from DateTime to linear numeric (0,1,2,3,...)
        df.index = pd.RangeIndex(start=0, stop=len(df))

        # Perform timezone conversion to EDT

        handleTime(df)

    df['Measured Water Level'] = df['Water Level']
    df['Water Level'] = df['Water Level'].apply(lambda x: round(x + offset, 2))
    df['VDatum'] = datum
    df['Offset'] = offset
    # Revert indexing from DateTime to linear numeric (0,1,2,3,...)
    df.index = pd.RangeIndex(start=0, stop=len(df))

    # Add unique Identifier to each data entry
    df['Identifier'] = df["SiteID"] + "-" + fileName[-4:] + "-" + df.reset_index().index.astype(str)
    df.to_csv(f"./Unfiltered_Data/{year}/{fileName}_Unfiltered.csv", index=False)
    return df


def handleTime(df):
    """
    Helper function to convert water level data from UTC to local timezone (EDT)

    Parameters:
      df (DataFrame): a formatted DF containing water level or high low data
    Returns:
      None
    """
    # Convert to datetime format
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    # Set local timezone to UTC
    df['Date Time'] = df['Date Time'].dt.tz_localize('UTC')
    # Convert timezone to EST
    df['Date Time'] = df['Date Time'].dt.tz_convert('US/Eastern')

    # Separate date and time
    df['Date'] = df['Date Time'].dt.date
    df['Time'] = df['Date Time'].dt.time


def finalFormatting(df: DataFrame):
    """
    Helper function to reformat and remove extraneous columns from the final report

    Parameters:
      df (DataFrame): a formatted DF containing water level or high low data
    Returns:
      None
    """
    # Rename columns
    df = df.rename(columns={'Water Level': 'Adjusted Water Level'})

    # Delete unnecessary columns
    df = df.drop(columns=['Date Time', 'Identifier'])

    # Reorder columns
    columns = ['Date', 'Time', 'SiteID', 'Source', 'Measured Water Level', 'Offset', 'Adjusted Water Level', 'VDatum']
    df = df[columns]

    return df
