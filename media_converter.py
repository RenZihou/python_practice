# -*- encoding: utf-8 -*-
# @Author: RZH

from typing import Union, List
from os import listdir, system, path, mkdir
from re import match, sub


def get_filenames(folder: Union[List[str], str],
                  ext: Union[List[str], str] = ('flv', 'wav', 'mp3'))\
        -> List[str]:
    folder = [folder] if isinstance(folder, str) else folder
    ext = [ext] if isinstance(ext, str) else ext
    pattern = r'^.*\.(%s)$' % '|'.join(ext)
    filenames = sum(map(lambda x: list(map(lambda f: '%s/%s' % (x, f), listdir(x))), folder), [])
    filenames = list(filter(lambda x: match(pattern, x), filenames))
    return filenames


def convert(src: List[str], dst: str = './output', ext: str = 'mp3') -> None:
    if not path.exists(dst):
        mkdir(dst)
    for file in src:
        new_name = sub(r'.*/', '%s/' % dst, sub(r'(?<=\.)\w+$', ext, file))
        system('ffmpeg -i "%s" -b:a 192k "%s"' % (file, new_name))
    return


if __name__ == '__main__':
    convert(get_filenames('', ))
    pass
