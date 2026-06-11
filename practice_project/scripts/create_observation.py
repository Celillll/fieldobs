import os
from datetime import date

# Settings
obs_number = 'OBS_001'
category = 'PLANTS'
today = date.today().strftime('%Y-%m-%d')

# Build folder name and path
folder_name = obs_number + '_' + today
folder_path = os.path.join('practice_project', '01_SORTED_OBSERVATIONS', category, folder_name)

# Create the folder
os.makedirs(folder_path, exist_ok=True)
print('Created folder: ' + folder_path)
