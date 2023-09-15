# import zipfile
# from lxml import etree

# def epub_info(fname):
#     def xpath(element, path):
#         return element.xpath(
#             path,
#             namespaces={
#                 "n": "urn:oasis:names:tc:opendocument:xmlns:container",
#                 "pkg": "http://www.idpf.org/2007/opf",
#                 "dc": "http://purl.org/dc/elements/1.1/",
#             },
#         )[0]

#     # prepare to read from the .epub file
#     zip_content = zipfile.ZipFile(fname)

#     # find the contents metafile
#     cfname = xpath(
#         etree.fromstring(zip_content.read("META-INF/container.xml")),
#         "n:rootfiles/n:rootfile/@full-path",
#     ) 

#     # grab the metadata block from the contents metafile
#     metadata = xpath(
#         etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata"
#     )

#     # repackage the data
#     return {
#         s: xpath(metadata, f"dc:{s}/text()")
#         for s in ("title", "language", "creator", "date", "identifier")
#     }
import sys
from pathlib import Path
from zipfile import ZipFile
from ebooklib import epub
from bs4 import BeautifulSoup
import shutil

epub_name = sys.argv[1]
output_dir_name = sys.argv[2]


book = epub.read_epub(epub_name)
epubFile = ZipFile(epub_name, "r")
output_dir_root = Path(output_dir_name)

epub_base_name = Path(epubFile.filename).stem
# print(epub_base_name)

output_dir = output_dir_root / epub_base_name
Path(output_dir).mkdir()

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
        extractedFile = epubFile.extract(imageSrc, output_dir_root)
        # print(extractedFile)
        output_name = "image%s%s" % (imageIdx, image_ext)
        imageIdx += 1
        # print(outputName)
        shutil.move(extractedFile, output_dir_root / epub_base_name / output_name)
