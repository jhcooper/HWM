import noaa_coops as nc
import pandas as pd


def retrieve_NOAA(begin_date, end_date, datum, stationID):
    begin_date = begin_date
    end_date = end_date
    product = 'high_low'
    datum = datum
    bin_num = None
    interval = None
    units = "english"
    time_zone = "lst"
    url = f'http://tidesandcurrents.noaa.gov/api/datagetter?begin_date={begin_date}&end_date={end_date}&station={stationID}&product={product}&datum={datum}&units={units}&time_zone={time_zone}&application=web_services&format=csv'
    print(url)
    tempStation = nc.Station(stationID)
    try:
        response = tempStation.get_data(begin_date, end_date, product, datum, bin_num, interval, units, time_zone)
    except ValueError as e:
        print(f"No data was found for station {stationID}: {e}")
        return None
    return response
