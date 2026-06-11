import os
from datetime import date

obs_number = 'OBS_001'
category = 'PLANTS'
today = date.today().strftime('%Y-%m-%d')
folder_path = os.path.join('practice_project', '01_SORTED_OBSERVATIONS', category, obs_number + '_' + today)

lines = [
    '# ' + obs_number + ' - ' + today,
    '',
    '## Species',
    'unknown',
    '',
    '## Location',
    'GPS: not recorded',
    '',
    '## Observations',
    '(write here)',
    '',
    '## Collected',
    'No'
]

output_path = os.path.join(folder_path, 'notes.md')
with open(output_path, 'w') as f:
    f.write('\n'.join(lines))
print('Created notes: ' + output_path)
