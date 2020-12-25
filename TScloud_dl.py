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


def set_cookie(session, url, share_id, pwd):
    """
    set cookies
    :param session: request session
    :param url: post url
    :param share_id: share_id
    :param pwd: password
    :return: updated session (with cookies)
    """
    get_r = session.get(url)
    csrf = findall(r'sfcsrftoken=(.+); ex', get_r.headers['set-cookie'])[0]
    form = {'token': share_id, 'password': pwd, 'csrfmiddlewaretoken': csrf}
    post_r = session.post(url, data=form)
    session.cookies.update(post_r.cookies)
    return session


def get_dl_url(session, base_url: str, file_path: str,
               folder: list = None, file: bool = True) -> list:
    """
    get all the files' link, including folders
    :param session: request session
    :param base_url: the root folder url
    :param file_path: the relative path of a folder
    :param folder: folders you want to download,
    `None` means all while `['']` means none
    :param file: whether download single file
    :return: a list of relative paths of the files to download
    """
    folder = [] if folder is None else folder
    dl_url = []
    print('[Info] Fetching files from .%s' % file_path)
    js = session.get(url=base_url + file_path).json()
    items: list = js['dirent_list']  # folders and files in current dictionary

    for each in items:
        if each['is_dir']:  # is folder
            if not (bool(folder) ^ (each['folder_name'] in folder)):
                # download folder
                dl_url += get_dl_url(session, base_url, each['folder_path'])
            else:
                print('[Warning] Skipped: ./%s' % each['folder_name'])
        elif file:  # is file & download file
            dl_url.append(each['file_path'])
    return dl_url


def dl_single(session, file_url: str, filepath: str) -> bool:
    """
    download a single file
    :param session: request session
    :param file_url: file url
    :param filepath: relative file path
    :return: `True` for downloaded successfully, `False` for no-permission
    """
    r = session.get(file_url, stream=True)
    if r.status_code == 404:  # no download permission
        print('[Fatal] Access Denied: %s' % filepath)
        return False
    dir_path = findall(r'^(.*)/.*$', filepath)[0]  # path without filename

    if not path.exists(dir_path):
        makedirs(dir_path)
    print('[Info] Downloading ./%s\n%s' % (filepath, file_url))
    with open(filepath, 'wb') as f:
        for data in tqdm(
                r.iter_content(chunk_size=4096),
                total=ceil(int(r.headers['Content-Length']) / 4096),
                unit='Mb', unit_scale=4096 * 1e-6
        ):
            f.write(data)
    return True


def dl_all(session, file_urls: list) -> int:
    """
    download all files
    :param session: request session
    :param file_urls: files' url
    :return: total files downloaded
    """
    count = 0
    for each in file_urls:
        count += dl_single(session, *each)
    print('%d files downloaded.' % count)
    return count


def main(share_id: str, pwd: str = None,
         folder: list = None, file: bool = True) -> bool:
    """
    download files from Tsinghua cloud share-link
    :param share_id: share link id, a string make up of alphanumerical chars
    :param pwd: [optional] password, the program will ask the user to input
    if a password is required but not given here
    :param folder: folders (in the root folder) to download,
    `None` means all while `['']` means none
    :param file: whether download single files in the root folder
    :return: `False` for no-permission
    """
    po_base_url = 'https://cloud.tsinghua.edu.cn/d/%s/' % share_id
    dl_base_url = 'https://cloud.tsinghua.edu.cn/d/%s/files/?p=' % share_id
    base_url = 'https://cloud.tsinghua.edu.cn/api/v2.1/share-links' \
               '/%s/dirents/?path=' % share_id
    dl_suffix = '&dl=1'
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; '
                                          'Trident/7.0; rv:11.0) like Gecko'})

    r = session.get(dl_base_url)
    if r.status_code == 404:  # invalid share-id
        print('[Fatal] Invalid Share-Id.')
        return False
    try:
        title: str = findall(r'<meta property="og:title" content="(.*)" />',
                             r.text)[0]  # root folder name
    except IndexError:
        print('[Warning] password required.')
        session = set_cookie(session, url=po_base_url, share_id=share_id,
                             pwd=pwd if pwd else input('password: '))
        r = session.get(dl_base_url)
        title: str = findall(r'<meta property="og:title" content="(.*)" />',
                             r.text)[0]  # root folder name
    else:
        pass

    relative_dl_urls: list = get_dl_url(
        session,
        base_url, file_path='%2F', folder=folder, file=file,
    )  # relative path to download
    dl_urls: list = list(map(
        lambda x: [dl_base_url + parse.quote(x) + dl_suffix, title + x],
        relative_dl_urls
    ))  # url to download, parse `x` to handle chinese characters and signs
    dl_all(session, dl_urls)
    return True


if __name__ == '__main__':
    main('SHARE_ID_HERE', pwd=None, folder=[], file=True)
    pass
