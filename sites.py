class Site:
    """
    Represents a monitoring site with specific attributes.

    Attributes:
      siteID (str): The unique identifier for the site.
      source (str): The source of the site data (e.g., NOAA or USGS).
      name (str): The name of the site.
      threshold (float, optional): A threshold value specific to the site (if applicable).
      offset (float): The offset value for the site.
      datum (str): The datum associated with the site.
    """

    def __init__(self, siteID: str, source: str, name: str, datum: str, offset: float, threshold: float = None):
        """
        Initializes a new instance of the Site class.

        Parameters:
          siteID (str): The unique identifier for the site.
          source (str): The source of the site data (e.g., NOAA or USGS).
          name (str): The name of the site.
          datum (str): The datum associated with the site.
          offset (float): The offset value for the site.
          threshold (float, optional): A threshold value specific to the site (if applicable).
        """
        self.siteID = siteID
        self.source = source
        self.name = name
        self.threshold = threshold
        self.offset = offset
        self.datum = datum


# NOAA Sites
Delaware_City = Site('8551762', 'NOAA', 'Delaware_City', "MSL", -0.04)
Lewes_Breakwater_Harbor = Site('8557380', 'NOAA', 'Lewes_Breakwater_Harbor', "NAVD", 0, 4.37)
Marcus_Hook = Site('8540433', 'NOAA', 'Marcus_Hook', "MSL", 0.15)
Ocean_City_Inlet = Site('8570283', 'NOAA', 'Ocean_City_Inlet', "NAVD", 0)
Reedy_Point = Site('8551910', 'NOAA', 'Reedy_Point', "NAVD", 0, 4.53)

# USGS Sites
Christina_River_Newport = Site('01480065', 'USGS', 'Christina_River_Newport', "NGVD", -1.05)
Christina_Wilmington = Site('01480120', 'USGS', 'Christina_Wilmington', "NGVD", -1.05)
Del_River_New_Castle = Site('01482170', 'USGS', 'Del_River_New_Castle', "NAVD", 0)
Murderkill_Bowers = Site('01484085', 'USGS', 'Murderkill_Bowers', "NAVD", 0, 4.50)
Murderkill_Frederica = Site('01484080', 'USGS', 'Murderkill_Frederica', "NGVD", -0.78)
Indian_River_Rosedale = Site('01484540', 'USGS', 'Indian_River_Rosedale', "NAVD", 0)
Indian_River_Bethany = Site('01484683', 'USGS', 'Indian_River_Bethany', "NAVD", 0)
Fred_Hudson_Bethany = Site('01484690', 'USGS', 'Fred_Hudson_Bethany', "NAVD", 0)
Vines_Crossing_Dagsboro = Site('01484549', 'USGS', 'Vines_Crossing_Dagsboro', "NAVD", 0)
Rehoboth_Bay_Dewey = Site('01484670', 'USGS', 'Rehoboth_Bay_Dewey', "NAVD", 0)
Jefferson_Crossing_Bethany = Site('01484696', 'USGS', 'Jefferson_Crossing_Bethany', "NAVD", 0)
Little_Assawoman_Fenwick = Site('01484701', 'USGS', 'Little_Assawoman_Fenwick', "NAVD", 0)

allSites = [Delaware_City, Lewes_Breakwater_Harbor, Marcus_Hook, Ocean_City_Inlet, Reedy_Point,
            Christina_River_Newport, Christina_Wilmington, Del_River_New_Castle, Murderkill_Bowers,
            Murderkill_Frederica,
            Indian_River_Rosedale, Indian_River_Bethany, Fred_Hudson_Bethany, Vines_Crossing_Dagsboro,
            Rehoboth_Bay_Dewey,
            Jefferson_Crossing_Bethany, Little_Assawoman_Fenwick]

usgsSites = [
    Christina_River_Newport, Christina_Wilmington, Del_River_New_Castle, Murderkill_Bowers,
    Murderkill_Frederica,
    Indian_River_Rosedale, Indian_River_Bethany, Fred_Hudson_Bethany, Vines_Crossing_Dagsboro,
    Rehoboth_Bay_Dewey,
    Jefferson_Crossing_Bethany, Little_Assawoman_Fenwick]

noaaSites = [Delaware_City, Lewes_Breakwater_Harbor, Marcus_Hook, Ocean_City_Inlet, Reedy_Point, Murderkill_Bowers]
