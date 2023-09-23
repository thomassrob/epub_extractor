def is_image(test_str):
    image_extensions = {"png", "webp", "jpg", "gif", "jpeg"}
    # image_extensions = {"jpg", "png", "webp", "jpeg", "gif"}
    for ext in image_extensions:
        if f'.{ext}' in test_str.lower():
            return True
    return False
