import os
from mergers import mergeUnfiltered, mergeEvents, mergeOnDate
from retrieval import getData
from filtering import createFiltered
from delete import deleteTempFolders
from graphing import graph
from sites import Site, allSites


def createReport(site: Site, plotting: bool, year: str, product: str):
    """
    Master function to create and save Unfiltered, Filtered, and Isolated Events csvs as well as a png plot of threshold
    exceedance for USGS or NOAA Water Level data

    Parameters:
      begin_date (str): the beginning date of the desired data range (YYYYMMDD)
      end_date (str): the ending date of the desired data range (YYYYMMDD)
      stationID (str): the station ID of the desired station
      source (str): the data source (USGS or NOAA)
      fileName (str): the location name and year (location_year)
      threshold (float): the threshold for a HWM at the target station
      product (str):  *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)
    Returns:
      None
    """

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
    # Retrieve, Convert, Rename, and Reformat Data
    df = getData(siteID, datum, offset, begin_date, end_date, source, fileName, year, product)

    if df is None:
        return
    if plotting:
        df = graph(df, fileName, source, threshold, year)

    # Filter Data, Creating and saving 'Filtered' and 'Isolated_Events'csv
    if site.threshold != None:
        createFiltered(df, threshold, fileName, year)


def createYearlyReport(year: int, product: str, plotting: bool = False, keep: str = "A", sites: [Site] = allSites):
    """
    Generates a yearly report for the specified year.

    Parameters:
      year (int): The year for which the report is generated.
      product (str):  *FOR NOAA DATA ONLY* the product being retrieved (water_level or high_low)
      plotting (bool, optional): Specifies whether to include plots in the report. Default is False.
      keep (str, optional): Specifies which temporary files to keep. Valid values are 'A' (keep all),
            'N' (keep none), or 'I' (keep isolated events). Default is 'A'.
      sites (List[Site], optional): A list of Site objects representing the sites to include in the report.
            Default is allSites, which includes all available sites.

    Returns:
      None
    """
    for site in sites:
        print("Processing " + site.name + " " + str(year))
        # Generate individual reports for each site
        createReport(site, plotting, year, product)

    # Merge unfiltered data for the year
    unfiltered = mergeUnfiltered(year)
    # Merge isolated events for the year
    isolated = mergeEvents(year)
    # Perform date matching for all sites
    mergeOnDate(unfiltered, isolated, year)
    # Delete temporary folders based on keep command
    deleteTempFolders(keep, year)

    print("Done Processing " + str(year))
