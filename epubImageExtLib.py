from pathlib import Path, PurePath

import cssutils
from bs4 import BeautifulSoup


def extract_images_from_string(content):
    soup = BeautifulSoup(content, features="lxml")
    return_list = []
    for imgtag in soup.find_all(['img', 'image', 'div']):
        if 'img' == imgtag.name:
            return_list.append(imgtag['src'])
        elif 'image' == imgtag.name:
            return_list.append(imgtag['xlink:href'])
        elif 'div' == imgtag.name:
            div_style = imgtag.get('style')
            if (not div_style is None):
                # div_style = imgtag['style']
                style = cssutils.parseStyle(div_style)
                url = style['background-image']
                url = url.replace('url(', '').replace(')', '')
                # style = imgtag['style']
                if (url):
                    return_list.append(url)
    return return_list

def resolve_path(src_path, rel_path):
    return_path = PurePath(src_path) / PurePath(rel_path)
    return return_path.relative_to(src_path)