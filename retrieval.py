import pandas as pd
import requests
import io
import noaa_coops as nc
from formatting import formatAndSave


def getData(stationID: str, datum: str, offset: float, begin_date: str, end_date: str, source: str, fileName: str,
            year: int, product: str):
    # Function to handle data retrieval from USGS or NOAA
    # Parameters:
    #   begin_date (str): the beginning date of the desired data range (YYYYMMDD)
    #   end_date (str): the ending date of the desired data range (YYYYMMDD)
    #   stationID (str): the station ID of the desired station
    #   source (str): the data source (USGS or NOAA)
    #   product (str): *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)
    # Returns:
    #    df (DataFrame): the csv file of the data, in pandas DF form

    # If the data is coming from USGS:
    if source == 'USGS':
        # Retrieve the raw data
        url = \
            f'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no={stationID}&period=&begin_date={begin_date[0:4]}-{begin_date[4:6]}-{begin_date[6:]}&end_date={end_date[0:4]}-{end_date[4:6]}-{end_date[6:]}'
        raw = requests.get(url)
        # Skip the header rows and parse the data using pandas
        df = pd.read_csv(io.StringIO(raw.content.decode('utf-8')), comment='#', delimiter='\t')
    else:
        # Retrieve the raw data
        df = retrieve_NOAA(begin_date, end_date, datum, stationID, product)

    # Universalize Format, localize, and save the Unfiltered Data
    if df is None:
        return
    df = formatAndSave(df, source, offset, datum, fileName, stationID, year, product)
    return df


def retrieve_NOAA(begin_date, end_date, datum, stationID, product):
    """
    Retrieves NOAA data for a specific station and time period.

    Parameters:
      begin_date (str): The start date in the format 'YYYYMMDD'.
      end_date (str): The end date in the format 'YYYYMMDD'.
      datum (str): The datum for the data (e.g., 'MLLW', 'NAVD', 'IGLD').
      stationID (str): The ID of the NOAA station.
      product (str): The desired data (either high_low or water_level)

    Returns:
      DataFrame or None: The retrieved data as a pandas DataFrame if successful, None otherwise.
    """
    begin_date = begin_date
    end_date = end_date
    product = product
    datum = datum
    bin_num = None
    interval = None
    units = "english"
    time_zone = "lst"
    url = f'http://tidesandcurrents.noaa.gov/api/datagetter?begin_date={begin_date}&end_date={end_date}&station={stationID}&product={product}&datum={datum}&units={units}&time_zone={time_zone}&application=web_services&format=csv'

    tempStation = nc.Station(stationID)

    try:
        response = tempStation.get_data(begin_date, end_date, product, datum, bin_num, interval, units, time_zone)
    except ValueError as e:
        return None
    return response
