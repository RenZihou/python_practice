# -*- encoding: utf-8 -*-
# @Author: RZH

import requests
import json
from re import findall
from time import sleep
from os import remove


def download_pixiv(url: str):
    img = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; '
                          'Trident/7.0; rv:11.0) like Gecko',
            'referer': 'https://www.pixiv.net/en/artworks/%s'
                       % findall(r'.*/(.*?)_.*$', url)[0]
        }
    ).content
    filename = findall(r'.*/(.*?)$', url)[0]
    with open(filename, 'wb') as f:
        f.write(img)
    return filename


def upload(file: str) -> tuple:
    authorization = 'YOUR_SM.MS_API_KEY'  # api key
    r = requests.post(
        url='https://sm.ms/api/v2/upload/',
        headers={'Authorization': authorization},
        files={'smfile': open(file, 'rb')}
    )
    if r.status_code == 200:
        return r.json()['data']['url'], r.json()['data']['hash']


def delete(img_hash: str):
    r = requests.get(
        url='https://sm.ms/api/v2/delete/%s' % img_hash
    )
    if r.status_code == 200:
        return r.json()


def enlarge(url: str):
    config = {
        'style': 'art',  # `art`(illustration) or `photo`
        'noise': '1',  # -1: none, 0: low, 1: medium, 2: high, 3: highest
        'x2': '2',  # 1: 2x, 2: 4x, 3: 8x, 4:16x (8x and 16x are for paid ver.)
        'input': url
    }
    api_key = 'YOUR_BIGJPG_API_KEY'

    # upload image
    r = requests.post(
        url='https://bigjpg.com/api/task/',
        headers={'X-API-KEY': api_key},
        data={'conf': json.dumps(config)}
    )

    print(r.json())
    tid = r.json()['tid']
    # remains = r.json()['remaining_api_calls']
    wait = int(r.json()['minute']) * 60  # seconds
    sleep(wait)

    # download enlarged image file
    while True:
        img_r = requests.get(
            url='https://bigjpg.com/api/task/%s' % tid,
            # headers={'X-API-KEY': api_key}
        )
        print(img_r.json())
        status = img_r.json()[tid]['status']
        if status == 'error':
            print('Error')
            return False
        elif status == 'new':
            print('Waiting')
            sleep(60)
            pass
        elif status == 'success':
            img_url = img_r.json()[tid]['url']
            print(img_url)
            img = requests.get(url=img_url).content
            filename = findall(r'.*/(.*?)$', url)[0]
            with open(filename, 'wb') as f:
                f.write(img)
            return True


def main(mode: str, content: str):
    """
    :param mode: `file`: use local file,
        `pixiv`: use pixiv image url (https://i.pximg.net/),
        `url`: use image url
    :param content: filename for `file` mode,
        image url for `pixiv` or `url` mode
    :return: None
    """
    if mode == 'file':  # local file
        img_url, img_hash = upload(content)
        remove(content)
        enlarge(img_url)
        delete(img_hash)
    elif mode == 'pixiv':  # pixiv artwork
        filename = download_pixiv(content)
        img_url, img_hash = upload(filename)
        remove(content)
        enlarge(img_url)
        delete(img_hash)
    elif mode == 'url':  # other links
        enlarge(content)
    return


if __name__ == '__main__':
    pass
