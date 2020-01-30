import requests
import sys
from datetime import datetime

url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_Europe_7d.csv'
r = requests.get(url, allow_redirects=True)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'modis_' + datetime.today().strftime('%Y%m%d') + '.csv'
open(filename, 'wb').write(r.content)
