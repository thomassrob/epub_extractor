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
import ebooklib
from zipfile import ZipFile
from ebooklib import epub
from ebooklib.utils import debug
from bs4 import BeautifulSoup as BS
import shutil

book = epub.read_epub(sys.argv[1])
epubFile = ZipFile(sys.argv[1], "r")
outputDir = sys.argv[2]

#debug(book.spine)

#page=book.get_item_with_id("p_0146")
#print(page)
#print(content)

imageIdx=0

for page in book.spine:
    id=page[0]
    item=book.get_item_with_id(id)
    content=item.get_body_content()
    soup = BS(content, features="lxml")
    for imgtag in soup.find_all('img'):
        print("imgtag")
        print(imgtag)
        print("imgtag src")
        print(imgtag['src'])
        rawSrc = imgtag['src']
        imageSrc = rawSrc.replace("../", "OEBPS/")
        extractedFile = epubFile.extract(imageSrc, outputDir)
        print(extractedFile)
        outputName = "image%s.jpg" % (imageIdx)
        imageIdx += 1
        print(outputName)
        shutil.move(extractedFile, outputName)
#    for name in epubFile.namelist():
#        print(name)

    
    #   for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
 #       print(image.get_name())
 #       if image.get_name() == imgSrc:
 #           print("Match")
    
#for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
#    print(image.get_id())


    
#print(page.get_links())
#print(sys.getsizeof(page.get_links()))
#print(page.is_chapter())
#for link in page.get_links():
#    print(1)
    #debug(link)
#images=page.get_links_of_type(ebooklib.ITEM_IMAGE)
#print(images)


#for page in book.spine:
#    debug(page)
#    id=page[0]
#    print(id)
#    item=book.get_item_with_id(id)
#    debug(item)
#    images=item.get_links()
#    print(images)

    #    for image in images:
#        print(image.get_type)
    
#    print(book.get_item_with_id(page[0]).get_links_of_type(1))
    #    for image in book.get_item_with_id(page[0]).get_links_of_type(1):
#        print(image)

#for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
#    print(image)
    
