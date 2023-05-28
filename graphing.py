from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def graph(df: DataFrame, fileName: str, source: str, threshold: float):
    # Generates a plot representation of water level at a site over a period of time compared to that site's threshold.
    # The generated plot is saved under 'filename_plot.png' in the 'Plots' Folder
    # Also makes a call to formatAndSave to first format the data and save the unfiltered data before manipulation.
    # Parameters:
    #   df: DataFrame - the csv file of the data, in pandas DF form
    #   source: str - the data source (USGS or NOAA)
    #   threshold: float - the threshold for a HWM at the target station
    # Returns:
    #    df: DataFrame - the csv file of the data, in pandas DF form, now universally formatted and localized

    # Isolate DateTime as 'date' and corresponding water level as 'WL'
    date = df["Date Time"]
    value = df["Water Level"]

    # Create Plot Object
    fig, ax = plt.subplots(figsize=(8, 6))

    # Locator for Major Axis
    half_year_locator = mdates.MonthLocator(interval=1)
    ax.xaxis.set_major_locator(half_year_locator)

    # Formatter for Major Axis (Four Digit Year, Two Digit Month)
    year_month_formatter = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(year_month_formatter)

    # Plot Data
    ax.plot(date, value)

    # Isolate Data Location as 'location' and Year as 'year' from filename
    location = fileName[:-5]
    year = fileName[-4:]

    # Set Title and Axis Labels
    ax.set_title(f'{location} High/Low Tides {year}')
    ax.set_ylabel('Water Level')
    ax.set_xlabel('Date')

    # Add Threshold Line
    if threshold != None:
        plt.axhline(y=threshold, color='r', linestyle='-')

    # Add Legend
    ax.legend(loc='lower left', title='Key', labels=['Water Level', 'Threshold'])

    # Formats X Labels
    fig.autofmt_xdate()

    # Export Final Graph as a png
    plt.savefig(f"./Plots/{fileName}_Plot.png")
    plt.close()
    return df
