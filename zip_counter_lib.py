import logging
import zipfile


def is_image(test_str):
    image_extensions = {"png", "webp", "jpg", "gif", "jpeg"}
    for ext in image_extensions:
        if f'.{ext}' in test_str.lower():
            logging.debug('String:<%s> matches extension <$s>', test_str, ext)
            return True
    logging.debug('String:<%s> does not match any image extension: %s', test_str, image_extensions)
    return False


def count_images_in_zip(zip_name):
    src_file = zipfile.ZipFile(zip_name)
    image_count = 0
    for zip_item in src_file.namelist():
        if is_image(zip_item):
            logging.debug("Found image: %s", zip_item)
            image_count += 1
    return image_count
