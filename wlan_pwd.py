# -*- encoding: utf-8 -*-
# @Author: RZH

import ctypes
import sys
from os import popen, path
from re import findall


def get_wlan_list() -> list:
    r = popen('netsh wlan show profile').read()
    wlan = findall(r'所有用户配置文件\s*:\s*(.+?)\n', r)
    return wlan


def get_detail(name: str) -> tuple:
    r = popen('netsh wlan show profile name="%s" key=clear' % name).read()
    # 身份验证，安全密钥，关键内容
    auth = findall(r'身份验证\s*:\s*(.+?)\n', r)[0]
    if findall(r'安全密钥\s*:\s*存在', r):
        key = findall(r'关键内容\s*:\s*(.+?)\n', r)[0]
    else:
        key = None
    return name, auth, key


def main(file: str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        f.write('name,auth_type,password\n')
        for each in get_wlan_list():
            f.write('%s,%s,%s\n' % get_detail(each))
    return None


if __name__ == '__main__':
    if ctypes.windll.shell32.IsUserAnAdmin():
        main(path.abspath('.') + '\\' + 'wlan_pwd.csv')
    else:
        # rerun this file as administrator
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
