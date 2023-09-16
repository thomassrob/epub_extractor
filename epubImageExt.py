#!/usr/bin/env python
import os
import sys
from pathlib import Path
from zipfile import ZipFile

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

epub_name = sys.argv[1]
output_dir_name = sys.argv[2]

if not (os.path.isfile(epub_name)):
    print("Epub file "+epub_name+" doesn't exist or isn't a file")
    exit(1)

if not (os.path.isdir(output_dir_name)):
    print("Output dir "+output_dir_name+" doesn't exist or isn't a directory")
    exit(1)


book = epub.read_epub(epub_name)
epubFile = ZipFile(epub_name, "r")
output_dir_root = Path(output_dir_name)

epub_base_name = Path(epubFile.filename).stem
# print(epub_base_name)

output_dir = output_dir_root / epub_base_name
Path(output_dir).mkdir()

imageIdx = 0


def get_image_map(src_book: epub) -> dict:
    images = src_book.get_items_of_type(ebooklib.ITEM_IMAGE)
    image_map = dict ()
    for image in images:
        image_map[image.file_name] = image.id
    return image_map


image_map = get_image_map(book)

for page in book.spine:
    page_id = page[0]
    item = book.get_item_with_id(page_id)
    content = item.get_body_content()
    soup = BeautifulSoup(content, features="lxml")

    covers = book.get_items_of_type(ebooklib.ITEM_COVER)
    cover_file = open(output_dir_root / epub_base_name / "00-cover.jpg", "wb")
    cover_file.write(next(covers).get_content())
    cover_file.close()

    for imgtag in soup.find_all('img'):
        rawSrc = imgtag['src']
        image_id = image_map.get(rawSrc)

        image_ext = Path(rawSrc).suffix
        image = book.get_item_with_id(image_id)

        output_name = "image%s%s" % (imageIdx, image_ext)
        image_file = open(output_dir_root / epub_base_name / output_name, "wb")
        image_file.write(image.get_content())
        image_file.close()
        imageIdx += 1
        # print(outputName)
#        shutil.move(extractedFile, output_dir_root / epub_base_name / output_name)


