import unittest
from unittest import TestCase

from zip_counter_lib import is_image


class TestIsImage(TestCase):
    def test_is_image(self):
        self.assertTrue(is_image("test.png"))
        self.assertFalse(is_image("testpng"))

    def test_is_image_webp(self):
        self.assertTrue(is_image("test.webp"))

    def test_is_image_jpg(self):
        self.assertTrue(is_image("test.jpg"))
    def test_is_image_gif(self):
        self.assertTrue(is_image("test.gif"))
    def test_is_image_jpeg(self):
        self.assertTrue(is_image("test.jpeg"))
        self.assertTrue(is_image("test.jPEg"))
    def test_neg_case(self):
        self.assertFalse(is_image("not an image"))

if __name__ == '__main__':
    unittest.main()
