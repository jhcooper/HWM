## HWMDB Report Generator

The HWMDB Report Generator is a Python script that generates a yearly report based on user inputs. It utilizes
the `createYearlyReport` function from the `report` module to generate the report.

### Usage

1. Ensure that you have Python installed on your system.

2. Clone the repository and navigate to the project directory.

3. Import the required modules and define the necessary classes.

4. Run the main script using the command `python main.py`.

5. Follow the prompts to provide the required inputs:

    - Enter a year (1962-Present): Enter the desired year for the report. The year must be between 1962 and the current
      year.

    - Do you want plots? (yes/no): Specify whether you want to include plots in the report. Enter "yes" or "no".

    - Which temporary files do you want to keep? (A for All/N for None/I for the Isolated Events/Enter for default (
      All)): Choose which temporary files to keep after generating the report. Enter "A" to keep all files, "N" to keep
      none, or "I" to keep only the isolated events.

    - Enter a list of site names (comma-separated) from the available sites, or press enter for all sites: Enter a
      comma-separated list of site names to include in the report. If no input is provided, the report will include all
      available sites.

6. The report will be generated based on the provided inputs and saved to the specified location.

Certainly! Here's an updated version of the dependencies section:

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
pip install pandas matplotlib noaa_coops
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