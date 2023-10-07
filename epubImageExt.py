#!/usr/bin/env python
import logging
import os
import sys
from pathlib import Path
from zipfile import ZipFile

import ebooklib
from ebooklib import epub

from epubImageExtLib import extract_images_from_string

logging.basicConfig(level=logging.INFO)


epub_name = sys.argv[1]
output_dir_name = sys.argv[2]

if not (os.path.isfile(epub_name)):
    logging.error("Epub file "+epub_name+" doesn't exist or isn't a file")
    exit(1)

if not (os.path.isdir(output_dir_name)):
    logging.error("Output dir "+output_dir_name+" doesn't exist or isn't a directory")
    exit(1)

logging.debug('Opening epub file: %s', epub_name)
book = epub.read_epub(epub_name)
epubFile = ZipFile(epub_name, "r")
output_dir_root = Path(output_dir_name)

epub_base_name = Path(epubFile.filename).stem
logging.debug('Base file name: %s', epub_base_name)

output_dir = output_dir_root / epub_base_name
Path(output_dir).mkdir()



def get_image_map(src_book: epub) -> dict:
    images = src_book.get_items_of_type(ebooklib.ITEM_IMAGE)
    image_map = dict ()
    for image in images:
        image_map[image.file_name] = image.id
    return image_map


image_map = get_image_map(book)

covers = book.get_items_of_type(ebooklib.ITEM_COVER)
try:
    single_cover = next(covers)
    image_map[single_cover.file_name] = single_cover.id
    cover_file = open(output_dir_root / epub_base_name / "00-cover.jpg", "wb")
    cover_file.write(single_cover.get_content())
    cover_file.close()
except StopIteration:
    logging.error("No cover")


def extract_all_images():
    imageIdx = 0
    processedImages = set()
    for page in book.spine:
        page_id = page[0]
        item = book.get_item_with_id(page_id)
        content = item.get_body_content()
        for image_name in extract_images_from_string(content):
            if not image_name in processedImages:
                image_id = image_map.get(image_name.replace('../', ''))
                logging.debug(f'rawStr: {image_name}')
                logging.debug(f'image_id: {image_id}')
                image_ext = Path(image_name).suffix
                image = book.get_item_with_id(image_id)
                image_idx_str = str(imageIdx).zfill(6)

                output_name = "image%s%s" % (image_idx_str, image_ext)
                image_file = open(output_dir_root / epub_base_name / output_name, "wb")
                image_file.write(image.get_content())
                image_file.close()
                imageIdx += 1
                processedImages.add(image_name)


def way_2():
    imageIdx = 0
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        imageIdxStr = str(imageIdx).zfill(6)
        image_ext = Path(image.file_name).suffix

        output_name = "image%s%s" % (imageIdxStr, image_ext)
        image_file = open(output_dir_root / epub_base_name / output_name, "wb")
        image_file.write(image.get_content())
        image_file.close()
        imageIdx += 1
        # processedImages.add(rawSrc)


# way_2()

extract_all_images()


