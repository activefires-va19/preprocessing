import csv
import os
import sys
from fnmatch import fnmatch
from pathlib import Path

if len(sys.argv) < 3:
    print("The script requires 2 arguments: <NASA_EARTHDATA_APP_KEY>, <OUTPUT_DIRECTORY>")
    exit(1)
else:
    app_key = sys.argv[1]
    folder = sys.argv[2]

os.system(
    'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=7 "https://nrt4.modaps.eosdis.nasa.gov/api/v2/content/archives/FIRMS/c6/Europe" '
    '--header "Authorization: Bearer ' + app_key + '" -P ' + folder)

files_name = []
for path, subdirs, files in os.walk(folder):
    for name in files:
        if fnmatch(name, "*.txt"):
            files_name.append(os.path.join(path, name))

line_written = 0
if len(files_name) == 0:
    exit(-1)
print(str(Path(files_name[0]).parent) + "/merged.csv")
with open(str(Path(files_name[0]).parent) + "/merged.csv", mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for file_name in files_name:
        with open(file_name, mode='r') as txt_file:
            csv_reader = csv.reader(txt_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0 and line_written == 0:
                    writer.writerow(row)
                    line_count += 1
                    line_written += 1
                else:
                    writer.writerow(row)
                    line_count += 1
                    line_written += 1
            print(f'Processed {line_count} lines from files')