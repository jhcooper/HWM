## HWMDB Report Generator

The HWMDB Report Generator is a Python script that generates a yearly report of the dates and water level data of all
High Water Mark Events in Delaware. A High Water Mark Event is identified based off of a water level threshold
excedance at one of the following sites: Lewes Breakwater Harbor, Reedy Point, or Murderkill Bowers. Once one of these
events is identified, the water level data from the rest of the sites across the State for the corresponding time window
is sourced and added to the final report. This tool also provides individual site plotting capabilities, enabling the
user to generate yearly charts for each site in order to easily visualize water levels across the State. Data for these
reports and plots is sourced from the NOAA and USGS APIs.

### Usage

1. Ensure that you have Python installed on your system.

2. Clone the repository and navigate to the project directory.

3. Import the required modules and define the necessary classes.

4. Run the main script using the command `python main.py`.

5. Follow the prompts to provide the required inputs:

    - Enter a year (1962-Present):
        - Enter the desired year for the report. The year must be between 1962 and the current
          year.

    - Do you want plots? (y/n)
        - Specify whether you want to include plots in the report. Enter "y" for "yes" or "n" for "no".

    - Which temporary files do you want to keep? (A for All/N for None/I for the Isolated Events/Enter for default (
      All)):
        - Choose which temporary files to keep after generating the report. Enter "A" to keep all files, "N" to keep
          none, or "I" to keep only the isolated events.

    - Enter a list of site names (comma-separated) from the available sites, or press enter for all sites
        - Enter a comma-separated list of site names to include in the report. If no input is provided, the report will
          include all
          available sites.
    - Would you like the NOAA data to be daily high-low data or hourly water level data? \n Enter: 'HL' for high-low or
      'WL' for hourly water level
        - Applies to NOAA Sites only. water_level refers to hourly water level data, while high_low refers to the highs
          and lows for each day.

6. The report will be generated based on the provided inputs and saved to the Yearly Reports folder.

### Dependencies

The script relies on the following modules:

- `os`: Provides functions for interacting with the operating system, used for file operations.

- `shutil`: Offers high-level file operations, used for file manipulation.

- `pandas`: Provides data manipulation and analysis tools, used for handling and processing data.

- `matplotlib.pyplot`: Offers a MATLAB-like plotting framework, used for creating plots in the report.

- `matplotlib.dates`: Provides functionality for working with dates and times in Matplotlib plots.

- `datetime.timedelta`: Represents a duration or difference between two dates or times, used for time calculations.

- `noaa_coops`: A Python library for accessing NOAA CO-OPS (Center for Operational Oceanographic Products and Services)
  data, used for retrieving data from NOAA CO-OPS API.

Please make sure to install these dependencies before running the script. You can use `pip` to install the required
packages:

```
# Install with pip
❯ pip install pandas matplotlib noaa_coops

# Install with poetry
❯ poetry add pandas matplotlib noaa_coops

# Install with conda
❯ conda install -c conda-forge pandas matplotlib noaa_coops
```

Note: The `noaa_coops` package may have additional dependencies that need to be installed as well.

### License

This project is licensed under the [University of Delaware License](LICENSE).

Feel free to modify and use the code according to your needs.

### Acknowledgments

This project was developed as part of a larger system and is based on the work of the contributors to the HWMDB (High
Water Mark Database) project.
The HWMDB is project through University of Delaware's Center for Environmental Monitoring & Analysis (CEMA).

For more information about CEMA and the HWMDB project, visit [cema.udel.edu](https://cema.udel.edu/).

If you encounter any issues or have any questions, please feel free
to [open an issue](https://github.com/jhcooper/HWM/issues) on the GitHub repository.

Thank you for using the HWMDB Report Generator!