class Site:
    def __init__(self, siteID: str, source: str, name: str, threshold: float = None):
        self.siteID = siteID
        self.source = source
        self.name = name
        self.threshold = threshold


# NOAA Sites
Delaware_City = Site('8551762', 'NOAA', 'Delaware_City')
Lewes_Breakwater_Harbor = Site('8557380', 'NOAA', 'Lewes_Breakwater_Harbor', 4.37)
Marcus_Hook = Site('8540433', 'NOAA', 'Marcus_Hook')
Ocean_City_Inlet = Site('8570283', 'NOAA', 'Ocean_City_Inlet')
Reedy_Point = Site('8551910', 'NOAA', 'Reedy_Point', 4.53)

# USGS Sites
Christina_River_Newport = Site('01480065', 'USGS', 'Christina_River_Newport')
Christina_Wilmington = Site('01480120', 'USGS', 'Christina_Wilmington')
Del_River_New_Castle = Site('01482170', 'USGS', 'Del_River_New_Castle')
Murderkill_Bowers = Site('01484085', 'USGS', 'Murderkill_Bowers', 4.50)
Murderkill_Frederica = Site('01484080', 'USGS', 'Murderkill_Frederica')
Indian_River_Rosedale = Site('01484540', 'USGS', 'Indian_River_Rosedale')
Indian_River_Bethany = Site('01484683', 'USGS', 'Indian_River_Bethany')
Fred_Hudson_Bethany = Site('01484690', 'USGS', 'Fred_Hudson_Bethany')
Vines_Crossing_Dagsboro = Site('01484549', 'USGS', 'Vines_Crossing_Dagsboro')
Rehoboth_Bay_Dewey = Site('01484670', 'USGS', 'Rehoboth_Bay_Dewey')
Jefferson_Crossing_Bethany = Site('01484696', 'USGS', 'Jefferson_Crossing_Bethany')
Little_Assawoman_Fenwick = Site('01484701', 'USGS', 'Little_Assawoman_Fenwick')

allSites = [Delaware_City, Lewes_Breakwater_Harbor, Marcus_Hook, Ocean_City_Inlet, Reedy_Point,
            Christina_River_Newport, Christina_Wilmington, Del_River_New_Castle, Murderkill_Bowers,
            Murderkill_Frederica,
            Indian_River_Rosedale, Indian_River_Bethany, Fred_Hudson_Bethany, Vines_Crossing_Dagsboro,
            Rehoboth_Bay_Dewey,
            Jefferson_Crossing_Bethany, Little_Assawoman_Fenwick]
