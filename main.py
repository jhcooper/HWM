from report import createYearlyReport
from sites import Site, Delaware_City, Lewes_Breakwater_Harbor, Marcus_Hook, Ocean_City_Inlet, Reedy_Point, \
    Christina_River_Newport, Christina_Wilmington, Del_River_New_Castle, Murderkill_Bowers, Murderkill_Frederica, \
    Indian_River_Rosedale, Indian_River_Bethany, Fred_Hudson_Bethany, Vines_Crossing_Dagsboro, Rehoboth_Bay_Dewey, \
    Jefferson_Crossing_Bethany, Little_Assawoman_Fenwick, allSites, usgsSites, noaaSites

if __name__ == '__main__':
    if __name__ == '__main__':
        # Prompt for year input
        print("Welcome to the HWMDB report generator. To generate a report, please follow the following steps:")
        while True:
            try:
                year = int(input("Enter a year (1962-Present): "))
                if 1962 <= year <= 2023:
                    break
                else:
                    print("Invalid year. Please enter a year between 1962 and 2023.")
            except ValueError:
                print("Invalid input. Please enter a valid year.")

        # Prompt for plotting input
        while True:
            plot_input = input("Do you want plots? (yes/no): ").lower()
            if plot_input in ["yes", "no", ""]:
                plotting = plot_input == "yes"
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        # Prompt for keep input
        while True:
            keep_input = input(
                "Which temporary files do you want to keep? (A for All/N for None/I for the Isolated Events/Enter for default (All)): ").upper()
            if keep_input in ["A", "N", "I", ""]:
                keep = keep_input
                break
            else:
                print("Invalid input. Please enter 'A', 'N', 'I', or press enter.")

        # Prompt for sites input
        while True:
            print("Active Sites:")
            print(site.name for site in allSites)
            sites_input = input(
                "Enter a list of site names (comma-separated) from the available sites, or press enter for all sites: ")
            if sites_input == "":
                sites = noaaSites
                break
            else:
                sites = [s.strip() for s in sites_input.split(",")]
                if all(site in allSites for site in sites):
                    break
                else:
                    print("Invalid site names. Please enter site names from the provided list.")

        createYearlyReport(year, plotting, keep, sites)
