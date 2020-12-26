# -*- encoding: utf-8 -*-
# @Author: RZH

from os import listdir
from re import match


def change_encoding(folder: str, ext: str, old: str, new: str) -> int:
    count = 0
    for file in listdir(folder):
        if match(r'.+\.%s$' % ext, file):
            with open('%s/%s' % (folder, file), 'r', encoding=old) as f:
                content = f.read()
            with open('%s/%s' % (folder, file), 'w', encoding=new) as f:
                f.write(content)
            count += 1
    return count


if __name__ == '__main__':
    change_encoding('.', 'txt', 'gb18030', 'utf-8')
    pass
