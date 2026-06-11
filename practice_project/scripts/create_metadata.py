import json
import os
from datetime import date

# Settings
obs_number = 'OBS_001'
category = 'PLANTS'
today = date.today().strftime('%Y-%m-%d')

# Build folder path
folder_path = os.path.join('practice_project', '01_SORTED_OBSERVATIONS', category, obs_number + '_' + today)

# Metadata content
metadata = {
    'observation_id': obs_number,
    'date': today,
    'category': category,
    'species': 'unknown',
    'gps_lat': None,
    'gps_lon': None,
    'notes': ''
}

# Write metadata.json into the observation folder
output_path = os.path.join(folder_path, 'metadata.json')
with open(output_path, 'w') as f:
    json.dump(metadata, f, indent=4)
print('Created metadata: ' + output_path)
