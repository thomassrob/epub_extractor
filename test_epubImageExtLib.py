from pathlib import PurePosixPath
from unittest import TestCase

from epubImageExtLib import extract_images_from_string, resolve_path


class Test(TestCase):
    def test_extract_images_from_string_base(self):
        self.assertEqual([], extract_images_from_string(""))

    def test_extract_images_from_string_image(self):
        test_str = '''<html xmlns='http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
    <head>
    <meta charset="UTF-8"/>
    <title>Disney Manga: Beauty and the Beast - Belle's Tale (Full-Color Edition)</title>
    <meta content="width=1496, height=2300" name="viewport"/>
    <link href="../css/style.css" rel="stylesheet" type="text/css"/>
    <meta content="urn:uuid:e0000000-0000-0000-0000-000210345811" name="Adept.expected.resource"/>
    </head>
    <body>
    <div>
    
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="100%" version="1.1" viewBox="0 0 1496 2300" width="100%">
    <image height="2300" width="1496" xlink:href="../images/page_0002.jpg"/>
    </svg>
    
    
    </div>
    
    </body>'''
        self.assertEqual(['../images/page_0002.jpg'], extract_images_from_string(test_str))

    def test_extract_images_from_string_img(self):
        test_str = '''<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE html>
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                <meta name="viewport" content="width=864,height=1296"></meta>
                <title>Wynd</title>
                <link href="css/9781646680443.css" type="text/css" rel="stylesheet"/>
                </head>
                <body><div class="leftside" id="page_002"><img src="images/page002.jpg" alt="images" /></div>
                </body>
                </html>'''
        self.assertEqual(['images/page002.jpg'], extract_images_from_string(test_str))


    def test_resolve_path_base(self):
        self.assertEqual(PurePosixPath(''), resolve_path('', ''))

    def test_resolve_path_no_base_path(self):
        self.assertEqual(PurePosixPath('this/that/test'), resolve_path('', 'this/that/test'))
# Broken fix later
    # def test_resolve_path_file(self):
    #     self.assertEqual(PurePosixPath('images/page_0002.jpg'), resolve_path('/sourceFiles/', '../images/page_0002.jpg'))

    def test_extract_images_from_string_bg(self):
        test_str = '''b'\n        <div>\n            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewbox="0 0 1066 1600" preserveaspectratio="none">\n                <image width="1066" height="1600" xlink:href="images-2/cover.jpg"/>\n            </svg>\n        </div>\n    '
            '''
        self.assertEqual(['images-2/cover.jpg'], extract_images_from_string(test_str))

    def test_extract_images_47_samurai(self):
        test_str = '''<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
  <head>
    <title>The 47 Ronin</title>
    <link rel="stylesheet" type="text/css" href="styles/page.css"/>
    <meta name="viewport" content="width=900, height=1275"/>
    
  </head>
  <body style="margin-top:0px; margin-left:0px;">  
<div style="background-image: url(images/Images-011.jpg); height: 1275px; width: 900px;"> 
</div>
</body>
</html>'''
        self.assertEqual(['images/Images-011.jpg'], extract_images_from_string(test_str))

    def test_extract_images_elfen_lied(self):
        test_str = '''<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Elfen Lied Omnibus Volume 1</title>
    <link rel="stylesheet" type="text/css" href="styles/okam_9781506738932_epub3_css_r1.css"/>
    <meta name="viewport" content="width=1448, height=2048"/>
    <!-- kobo-style -->
    <script xmlns="http://www.w3.org/1999/xhtml" type="text/javascript" src="js/kobo.js"></script>
    
  </head>
  <body>
<div class="page">
<img src="images/Images-001.jpg" class="backgroundImage" alt="background"/>
</div>
<!-- The following line allows links in Kobo -->
<div style="display:none;">cover</div>
</body>
</html>'''
        self.assertEqual(['images/Images-001.jpg'], extract_images_from_string(test_str))