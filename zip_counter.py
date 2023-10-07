#!/usr/bin/env python
import logging
import sys
import zipfile

from zip_counter_lib import count_images_in_zip
logging.basicConfig(level=logging.INFO)

for zip_name in sys.argv[1:]:
    # zip_name = sys.argv[1]

    if not (zipfile.is_zipfile(zip_name)):
        logging.error("Zip file "+zip_name+" doesn't exist or isn't a file. Skipping")
        # exit(1)
    else:
        num_images = count_images_in_zip(zip_name)

        logging.info(f'{zip_name}: {num_images}')
