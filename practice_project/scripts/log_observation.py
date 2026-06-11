import csv
import os
from datetime import date

# Settings
obs_number = 'OBS_001'
category = 'PLANTS'
today = date.today().strftime('%Y-%m-%d')
species = 'unknown'
gps_lat = ''
gps_lon = ''
notes = ''

# CSV path
csv_path = os.path.join('practice_project', '03_DATA', 'observations.csv')

# New row
new_row = [obs_number, today, category, species, gps_lat, gps_lon, notes]

# Append to CSV
with open(csv_path, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(new_row)
print('Logged: ' + str(new_row))
