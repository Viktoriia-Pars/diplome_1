import requests
import datetime
from pprint import pprint
today_sec = int(datetime.datetime.now().timestamp())
two_day_sec = today_sec - 172800
url = "https://api.stackexchange.com/2.3/questions"
params = {'fromdate': str(two_day_sec),'todate': str(today_sec), 'order': 'desc', 'sort': 'activity','tagged': 'python', 'site': 'stackoverflow'}
r = requests.get(url = url, params = params)
res = r.json()
pprint(res)