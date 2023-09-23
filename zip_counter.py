#!/usr/bin/env python
import sys
import zipfile

from zip_counter_lib import is_image

for zip_name in sys.argv[1:]:
    # zip_name = sys.argv[1]

    if not (zipfile.is_zipfile(zip_name)):
        print("Zip file "+zip_name+" doesn't exist or isn't a file")
        # exit(1)
    else:
        src_file = zipfile.ZipFile(zip_name)

        num_images = 0

        for zip_item in src_file.namelist():
            if is_image(zip_item):
                num_images += 1

        print(f'{zip_name}: {num_images}')