import os, json, csv, shutil, sys
from datetime import date

# Input
if len(sys.argv) < 3:
    print('Usage: python new_observation.py OBS_002 FUNGI photo_002.jpg')
    sys.exit(1)

obs_number = sys.argv[1]
category = sys.argv[2]
photo = sys.argv[3] if len(sys.argv) > 3 else None
today = date.today().strftime('%Y-%m-%d')

# Paths
base = 'practice_project'
folder_path = os.path.join(base, '01_SORTED_OBSERVATIONS', category, obs_number + '_' + today)

# 1. Create folder
os.makedirs(folder_path, exist_ok=True)
print('Created: ' + folder_path)

# 2. Copy photo
if photo:
    src = os.path.join(base, '00_INBOX', 'photos_unsorted', photo)
    dst = os.path.join(folder_path, photo)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print('Copied: ' + photo)
    else:
        print('WARNING: photo not found in inbox: ' + photo)

# 3. Create metadata.json
metadata = {'observation_id': obs_number, 'date': today, 'category': category, 'species': 'unknown', 'gps_lat': None, 'gps_lon': None, 'notes': ''}
with open(os.path.join(folder_path, 'metadata.json'), 'w') as f:
    json.dump(metadata, f, indent=4)
print('Created: metadata.json')

# 4. Create notes.md
lines = ['# ' + obs_number + ' - ' + today, '', '## Species', 'unknown', '', '## Location', 'GPS: not recorded', '', '## Observations', '(write here)', '', '## Collected', 'No']
with open(os.path.join(folder_path, 'notes.md'), 'w') as f:
    f.write('\n'.join(lines))
print('Created: notes.md')

# 5. Log to CSV
csv_path = os.path.join(base, '03_DATA', 'observations.csv')
with open(csv_path, 'a', newline='') as f:
    csv.writer(f).writerow([obs_number, today, category, 'unknown', '', '', ''])
print('Logged to CSV')

print('Done. GPS and species still need to be filled in.')
