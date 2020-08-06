# -*- encoding: utf-8 -*-
# @Author: RZH

import requests
import json
from re import findall
from time import sleep

test_url = ''
# TODO: Upload image file to an image host and pass its url to `enlarge()`


def enlarge(url: str):
    config = {
        'style': 'art',
        'noise': '1',
        'x2': '2',
        'input': url
    }
    api_key = 'YOUR_API_KEY'

    r = requests.post(
        url='https://bigjpg.com/api/task/',
        headers={'X-API-KEY': api_key},
        data={'conf': json.dumps(config)}
    )

    print(r.json())
    tid = r.json()['tid']
    remains = r.json()['remaining_api_calls']
    wait = int(r.json()['minute']) * 60  # seconds
    sleep(wait)

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


if __name__ == '__main__':
    print(enlarge(test_url))
    pass
