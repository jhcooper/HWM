# Code to plot Annual HH WL for NOAA gauge and overlay threshold value

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# station id options 
# Lewes station id = 8557380   (4.37 ft)
# Reedy Point station id = 8551910 (4.53 ft)

stations = { 
    0: {"id": "8557380", "name": "Lewes", "threshold_m": 1.331976}, 
    1: {"id": "8551910", "name": "Reedy Point", "threshold_m": 1.380744 }
    }

selectedStation = 0
yr = '2016'
stationid = stations[selectedStation]['id']
stationName = stations[selectedStation]['name']
threshold = stations[selectedStation]['threshold_m']

'''
infile is downloaded from NOAA
http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20160601&end_date=20160630&station=8557380&product=high_low&datum=navd&units=metric&time_zone=lst&application=web_services&format=csv
'''
infile = 'coops_annual_hilo_{}_{}.csv'.format(stationid,yr) 
df = pd.read_csv(infile)
print(df.head())

# remove extra columns (not necessary columns)
df = df.drop(df.columns[[0, 4, 5]],axis = 1)
df = df.rename(columns={'Date Time':'DateTime',' Water Level':'WL'})

# convert to datetime
df["date"] = pd.to_datetime(df["DateTime"])

# select on Higher High water records
date = df["date"][df['TY'] == 'HH']
value = df["WL"][df['TY'] == 'HH']

# set up plot
fig, ax = plt.subplots(figsize=(8, 6))

# separate year into monthly groupings
half_year_locator = mdates.MonthLocator(interval=1)
# format for date
year_month_formatter = mdates.DateFormatter("%Y-%m") # four digits for year, two for month

#set axes
ax.xaxis.set_major_locator(half_year_locator) # Locator for major axis only.
ax.xaxis.set_major_formatter(year_month_formatter) # formatter for major axis only


ax.plot(date, value);
titleText = '{} Higher High Water Levels for {}'.format(stationName, yr)
ax.set_title(titleText)

# add threshold line (4.37 ft = 1.331976 m)
# specifying horizontal line type
plt.axhline(y = threshold, color = 'r', linestyle = '-')

# Rotates and right aligns the x labels. 
# Also moves the bottom of the axes up to make room for them.
fig.autofmt_xdate()
