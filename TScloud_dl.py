# -*- encoding: utf-8 -*-
# @Author: RZH

"""
Download files from Tsinghua Cloud share-link with a single click
"""

import requests
from os import makedirs, path
from re import findall
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
    items: list = js['dirent_list']

    print('Fetching files from %s' % file_path)
    for each in items:
        if each['is_dir']:
            if not (bool(folder) ^ (each['folder_name'] in folder)):
                dl_url += get_dl_url(
                    base_url,
                    each['folder_path'],
                )
        elif file:
            dl_url.append(each['file_path'])
    return dl_url


def dl_single(file_url: str, filepath: str) -> None:
    """
    download a single file
    :param file_url: file url
    :param filepath: relative file path
    :return: None
    """
    r = requests.get(file_url, headers=headers)
    dir_path = findall(r'^(.*)/.*$', filepath)[0]

    if not path.exists(dir_path):
        makedirs(dir_path)
    print('Downloading %s\n%s' % (filepath, file_url))
    with open(filepath, 'wb') as f:
        for data in tqdm(r.iter_content(chunk_size=1024)):
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
    dl_url = 'https://cloud.tsinghua.edu.cn/d/%s/files/?p=' % share_id
    base_url = 'https://cloud.tsinghua.edu.cn/api/v2.1/share-links' \
               '/%s/dirents/?path=' % share_id
    dl_suffix = '&dl=1'

    title = findall(
        r'<meta property="og:title" content="(.*)" />',
        requests.get(dl_url, headers=headers).text
    )[0]
    relative_dl_urls = get_dl_url(
        base_url, file_path='%2F', folder=folder, file=file
    )
    dl_urls = list(map(
        lambda x: [dl_url + x + dl_suffix, title + x],
        relative_dl_urls
    ))
    dl_all(dl_urls)
    return None


if __name__ == '__main__':
    main(input().strip(), folder=None, file=False)
    pass
