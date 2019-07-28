import pprint
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='CZ5LHN6CF6G8JFD8')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_daily_adjusted('DAI')

with open('test.txt','w') as fp:
    fp.write(str(pprint.pformat(data)))
    fp.write("\n")
    fp.write(str(pprint.pformat(meta_data)))