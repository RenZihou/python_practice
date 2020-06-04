# -*- encoding: utf-8 -*-
# @Author: RZH

import ctypes
import sys
from os import popen
from re import findall


def get_wlan_list() -> list:
    """
    get the list of wlan names that PC has connected once before
    :return: List[str]
    """
    r = popen('netsh wlan show profile').read()
    wlan = findall(r'所有用户配置文件\s*:\s*(.+?)\n', r)
    return wlan


def get_detail(name: str) -> tuple:
    """
    get the password of the wlan named `name`
    requires running this file as administrator
    :param name: the wlan name
    :return: Tuple[str], (name, auth_type, pwd)
    """
    r = popen('netsh wlan show profile name="%s" key=clear' % name).read()
    auth = findall(r'身份验证\s*:\s*(.+?)\n', r)[0]
    if findall(r'安全密钥\s*:\s*存在', r):
        key = findall(r'关键内容\s*:\s*(.+?)\n', r)[0]
    else:
        key = None
    return name, auth, key


def main(file: str = 'wlan_pwd.csv') -> None:
    with open(file, 'w', encoding='utf-8') as f:
        f.write('name,auth_type,password\n')
        for each in get_wlan_list():
            f.write('%s,%s,%s\n' % get_detail(each))
    return None


if __name__ == '__main__':
    if ctypes.windll.shell32.IsUserAnAdmin():  # is running as administrator
        main()
    else:
        # run this file as administrator
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
