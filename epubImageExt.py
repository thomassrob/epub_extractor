#!/usr/bin/env python
import os
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile
from ebooklib import epub
from bs4 import BeautifulSoup
import shutil

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

temp_dir = tempfile.TemporaryDirectory()
# Path(temp_dir).mkdir()

# debug(book.spine)

# page=book.get_item_with_id("p_0146")
# print(page)
# print(content)

imageIdx = 0

for page in book.spine:
    page_id = page[0]
    item = book.get_item_with_id(page_id)
    content = item.get_body_content()
    soup = BeautifulSoup(content, features="lxml")
    for imgtag in soup.find_all('img'):
        # print("imgtag")
        # print(imgtag)
        # print("imgtag src")
        # print(imgtag['src'])
        rawSrc = imgtag['src']
        imageSrc = rawSrc.replace("../", "OEBPS/")
        image_ext = Path(imageSrc).suffix
        extractedFile = epubFile.extract(imageSrc, temp_dir.name)
        # print(extractedFile)
        output_name = "image%s%s" % (imageIdx, image_ext)
        imageIdx += 1
        # print(outputName)
        shutil.move(extractedFile, output_dir_root / epub_base_name / output_name)

temp_dir.cleanup()