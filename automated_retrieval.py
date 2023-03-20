import noaa_coops as nc


def retrieve_NOAA(begin_date, end_date, stationID, product):
    begin_date = begin_date
    end_date = end_date
    product = product
    datum = "NAVD"
    bin_num = None
    interval = None
    units = "metric"
    time_zone = "lst"
    tempStation = nc.Station(stationID)
    response = tempStation.get_data(begin_date, end_date, product, datum, bin_num, interval, units, time_zone)
    return response
