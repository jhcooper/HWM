from pprintpp import pprint as pp
from noaa_coops import Station
import pandas as pd

'''
Retrieve High/Low data from the CO-OPS gauges and save locally

Lewes Station = 8557380
Reedy Point station = 8551910
'''

lewes = Station(id="8557380")
reedypt = Station(id="8551910")

stationlist = [lewes,reedypt]

yr = 2017

for s in stationlist:
	wlstation = s
	print(wlstation.name)
	print(wlstation.id)
    
	pp(wlstation.flood_levels)
	#pp(list(wlstation.metadata.items())[:5]) 
	#pp(wlstation.data_inventory)

	# http://tidesandcurrents.noaa.gov/api/datagetter?begin_date=20160601&end_date=20160630&station=8557380&product=high_low&datum=navd&units=metric&time_zone=lst&application=web_services&format=csv
	targetURL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={}0101&end_date={}1231&station={}&product=high_low&datum=NAVD&time_zone=lst&units=metric&application=UDstudent&format=csv".format(yr,yr,s.id)
	print(targetURL)

	df = pd.read_csv(targetURL)
	outfile = 'coops_annual_hilo_{}_{}.csv'.format(s.id,yr)
	print(outfile)
	df.to_csv(outfile)

	print(df)


