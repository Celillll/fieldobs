import shutil
import os

source = 'practice_project/00_INBOX/photos_unsorted/photo_001.jpg'
destination = 'practice_project/01_SORTED_OBSERVATIONS/PLANTS/photo_001.jpg'

shutil.copy2(source, destination)
print('Photo copied successfully')
