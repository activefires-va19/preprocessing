import csv
import sys
from datetime import datetime
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import reverse_geocoder as rg
import pycountry
import time

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = 'modis_' + datetime.today().strftime('%Y%m%d') + '.csv'

if len(sys.argv) > 2:
    out_file = sys.argv[2]
else:
    out_file = 'out_modis_' + datetime.today().strftime('%Y%m%d') + '.csv'
Path(Path(file).parent).mkdir(parents=True, exist_ok=True)
Path(Path(out_file).parent).mkdir(parents=True, exist_ok=True)

data = []
with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            header = row
        else:
            data.append(row)
            line_count += 1
    print(f'Processed {line_count} lines from files')

coordinates = []
for el in data:
    coordinates.append((el[0], el[1]))
results = rg.search(coordinates)
countries = []
for el in results:
    try:
        countries.append(pycountry.countries.get(alpha_2=el['cc']).name.replace(",", ""))
    except:
        if el['cc'] == 'XK':
            countries.append('Kosovo')
        else:
            countries.append(el['cc'])
index = 0
for el in data:
    el.insert(0, countries[index])
    index += 1

header.insert(0, 'Country')
data_for_pca = []
for el in data:
    acquire_time = el[header.index('acq_time')]
    pca_time = int(acquire_time[0:2]) * 60
    pca_time = pca_time + int(acquire_time[2:])
    pca_date = time.mktime(datetime.strptime(el[header.index('acq_date')], "%Y-%m-%d").timetuple())
    data_for_pca.append(
        [float(el[header.index('latitude')]), float(el[header.index('longitude')]),
         float(el[header.index('brightness')]),float(el[header.index('scan')]), float(el[header.index('track')]),
         pca_time, pca_date, float(el[header.index('bright_t31')]), float(el[header.index('frp')])])
scaled_data_for_pca = StandardScaler().fit_transform(data_for_pca)
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(scaled_data_for_pca)
"""
from matplotlib import pyplot as plt
plt.plot(principalComponents[:, 0], principalComponents[:, 1], 'o', markersize=3, color='blue', alpha=0.5,
         label='PCA transformed data in the new 2D space')
plt.xlabel('Y1')
plt.ylabel('Y2')
plt.xlim([-10, 20])
plt.ylim([-5, 20])
plt.legend()
plt.title('Transformed data from sklearn.decomposition import PCA')
plt.show()
"""
with open(out_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    lenComponents = len(principalComponents)
    index = 0
    for el in data:
        if index == 0:
            header.extend(["PCA component1", "PCA component2"])
            writer.writerow(header)
        el.extend(principalComponents[index])
        writer.writerow(el)
        index += 1
