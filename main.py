import os
from mergers import mergeUnfiltered, mergeEvents, mergeOnDate
from retrieval import getData
from filtering import filter_df, filter_on_day
from sites import Site, Delaware_City, Lewes_Breakwater_Harbor, Marcus_Hook, Ocean_City_Inlet, Reedy_Point, \
    Christina_River_Newport, Christina_Wilmington, Del_River_New_Castle, Murderkill_Bowers, Murderkill_Frederica, \
    Indian_River_Rosedale, Indian_River_Bethany, Fred_Hudson_Bethany, Vines_Crossing_Dagsboro, Rehoboth_Bay_Dewey, \
    Jefferson_Crossing_Bethany, Little_Assawoman_Fenwick, allSites, usgsSites, noaaSites


def createReport(site: Site, year: str):
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

    # Create Needed Parameters
    year_str = str(year)
    begin_date = year_str + '0101'
    end_date = year_str + '1231'
    siteID = site.siteID
    source = site.source
    fileName = site.name + '_' + year_str
    threshold = site.threshold
    datum = site.datum
    offset = site.offset

    # Predefine Isolated File Path
    isolated_events_path = f'./Isolated_Events/{fileName}_Events.csv'

    # Retrieve, Convert, Rename, and Reformat Data
    df = getData(siteID, datum, offset, begin_date, end_date, source, fileName, year)

    if df is None:
        return

    # df = graph(df, fileName, source, threshold)

    # Filter Data, Creating and saving 'Filtered' and 'Isolated_Events'csv
    if site.threshold != None:
        filtered = filter_df(df, threshold, fileName)
        filtered.to_csv(isolated_events_path)


def createYearlyReport(year: int, sites: [Site] = allSites, saveFiles: bool = False):
    for site in sites:
        print(site.name)
        createReport(site, year)

    unfiltered = mergeUnfiltered(year)

    folder_path = f'./Unfiltered_Data/{year}'

    for file_name in os.listdir(folder_path):
        if file_name.endswith(f'{year}.csv'):
            os.remove(os.path.join(folder_path, file_name))

    isolated = mergeEvents(year)

    mergeOnDate(unfiltered, isolated, year)


if __name__ == '__main__':
    for i in range(2016, 2023):
        createYearlyReport(i, noaaSites)
