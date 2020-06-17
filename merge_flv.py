# -*- encoding: utf-8 -*-
# @Author: RZH

from re import findall
from os import system, listdir, rename, remove


def rename_all():
    """
    ffmpeg doesn't support Chinese characters in filename
    :return: None
    """
    for file in listdir('.'):
        rename(file, ''.join(findall('[\x00-\xff]', file)).replace(' ', ''))
    return None


def group_files() -> dict:
    """
    :return: {title: [flv_file_1, flv_file_2, ...], ...}
    """
    groups = {}
    ass_files = filter(lambda x: x[-3:] == 'ass', listdir('.'))
    flv_files = sorted(list(filter(lambda x: x[-3:] == 'flv', listdir('.'))))
    for ass_file in ass_files:
        title = ass_file[:-4]
        groups[title] = []
        for flv_file in flv_files:
            if findall(r'^%s' % title, flv_file):
                groups[title].append(flv_file)
    return groups


def merge_all(src: dict, delete_ori: bool = False):
    """
    :param src: {title: [flv_file_1, flv_file_2, ...], ...}
    :param delete_ori: delete the old file (after merging them) or not
    :return: None
    """
    for title, files in src.items():
        with open('merge.txt', 'w', encoding='utf-8') as f:
            f.write("file '" + "'\nfile '".join(files) + "'")
        system('ffmpeg -f concat -i merge.txt -c copy %s' % title + '.flv')
        if delete_ori:
            for file in files:
                remove(file)
    remove('merge.txt')
    return None


if __name__ == '__main__':
    rename_all()
    merge_all(group_files(), delete_ori=True)
    pass
