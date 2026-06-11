import os
import json

# Path to sorted observations
base_path = os.path.join('practice_project', '01_SORTED_OBSERVATIONS')

missing = []

# Walk through all category folders
for category in os.listdir(base_path):
    category_path = os.path.join(base_path, category)
    if not os.path.isdir(category_path):
        continue
    for obs_folder in os.listdir(category_path):
        obs_path = os.path.join(category_path, obs_folder)
        if not os.path.isdir(obs_path):
            continue
        metadata_file = os.path.join(obs_path, 'metadata.json')
        if not os.path.exists(metadata_file):
            missing.append(obs_folder + ': NO metadata.json')
            continue
        with open(metadata_file) as f:
            data = json.load(f)
        if data.get('gps_lat') is None:
            missing.append(obs_folder + ': missing GPS')
        if data.get('species') == 'unknown':
            missing.append(obs_folder + ': species unknown')

if missing:
    print('Incomplete observations:')
    for item in missing:
        print('  - ' + item)
else:
    print('All observations complete')
