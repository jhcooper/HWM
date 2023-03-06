import requests
import pandas as pd
import io
bowers_url = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00065=on&format=rdb&site_no=01484085&period=&begin_date=2016-06-01&end_date=2017-05-31'
bowers_raw = requests.get(bowers_url)

# Skip the header rows and parse the data using pandas
df = pd.read_csv(io.StringIO(bowers_raw.content.decode('utf-8')), skiprows=26, delimiter='\t')
df = df.drop(0)
df.rename(columns={'69431_00065': 'Water Level', 'datetime' : 'Date Time'}, inplace=True)

print(df.head)