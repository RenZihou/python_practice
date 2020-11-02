# -*- encoding: utf-8 -*-
# @Author: RZH

"""
Download files from Tsinghua Cloud share-link with a single click
"""

import requests
from os import makedirs, path
from re import findall
from math import ceil
from urllib import parse
from tqdm import tqdm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; '
                         'Trident/7.0; rv:11.0) like Gecko'}


def get_dl_url(
        base_url: str, file_path: str, folder: list = None, file: bool = True
) -> list:
    """
    get all the files' link, including folders
    :param base_url: the root folder url
    :param file_path: the relative path of a folder
    :param folder: folders you want to download,
    `None` means all while `['']` means none
    :param file: whether download single file
    :return: a list of relative paths of the files to download
    """
    if folder is None:
        folder = []
    dl_url = []
    js = requests.get(url=base_url + file_path, headers=headers).json()
    items: list = js['dirent_list']  # folders and files in current dictionary

    print('Fetching files from %s' % file_path)
    for each in items:
        if each['is_dir']:  # is folder
            if not (bool(folder) ^ (each['folder_name'] in folder)):
                # download folder
                dl_url += get_dl_url(
                    base_url,
                    each['folder_path'],
                )
        elif file:  # is file && download file
            dl_url.append(each['file_path'])
    return dl_url


def dl_single(file_url: str, filepath: str) -> None:
    """
    download a single file
    :param file_url: file url
    :param filepath: relative file path
    :return: None
    """
    r = requests.get(file_url, headers=headers, stream=True)
    dir_path = findall(r'^(.*)/.*$', filepath)[0]  # path without filename

    if not path.exists(dir_path):
        makedirs(dir_path)
    print('Downloading %s\n%s' % (filepath, file_url))
    with open(filepath, 'wb') as f:
        for data in tqdm(
            r.iter_content(chunk_size=4096),
            total=ceil(int(r.headers['Content-Length']) / 4096),
            unit='Mb', unit_scale=4096 * 1e-6
        ):
            f.write(data)
    return None


def dl_all(file_urls: list) -> None:
    """
    download all files
    :param file_urls: files' url
    :return: None
    """
    for each in file_urls:
        dl_single(*each)
    return None


def main(share_id: str, folder: list = None, file: bool = True) -> None:
    """
    download files from Tsinghua cloud share-link
    :param share_id: share link id, a string make up of alphanumerical chars
    :param folder: folders (in the root folder) to download,
    `None` means all while `['']` means none
    :param file: whether download single files in the root folder
    :return: None
    """
    dl_base_url = 'https://cloud.tsinghua.edu.cn/d/%s/files/?p=' % share_id
    base_url = 'https://cloud.tsinghua.edu.cn/api/v2.1/share-links' \
               '/%s/dirents/?path=' % share_id
    dl_suffix = '&dl=1'

    title: str = findall(
        r'<meta property="og:title" content="(.*)" />',
        requests.get(dl_base_url, headers=headers).text
    )[0]  # root folder name
    relative_dl_urls: list = get_dl_url(
        base_url, file_path='%2F', folder=folder, file=file
    )  # relative path to download
    dl_urls: list = list(map(
        lambda x: [dl_base_url + parse.quote(x) + dl_suffix, title + x],
        relative_dl_urls
    ))  # url to download, parse `x` to handle chinese characters and signs
    dl_all(dl_urls)
    return None


if __name__ == '__main__':
    main('', folder=[''], file=True)
    pass
