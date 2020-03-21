# -*- coding: utf-8 -*-
# @Author: RZH

# TODO: add file type filter
# TODO: add process monitor

import os

JPG_HEADER = (0xFF, 0xD8)
PNG_HEADER = (0x89, 0x50)


def get_xor_code(sample_file: str) -> int:
    with open(sample_file, 'rb') as f:
        header = tuple(f.read(2))
    if header[0] ^ JPG_HEADER[0] == header[1] ^ JPG_HEADER[1]:
        return header[0] ^ JPG_HEADER[0]
    else:
        return header[0] ^ PNG_HEADER[0]


def decode_file(src_file: str, dst_file: str, xor_code: int) -> bool:
    new_byte = list()
    with open(src_file, 'rb') as f:
        for byte in f.read():
            new_byte.append(byte ^ xor_code)
    suffix = '.jpg' if new_byte[0] == JPG_HEADER[0] else '.png'
    with open(dst_file.replace('.dat', suffix), 'wb') as f:
        f.write(bytes(new_byte))
    return True


def main(src: str, dst: str):
    files = os.listdir(src)
    xor_code = get_xor_code(src + '/' + files[0])
    for file in files:
        decode_file(src + '/' + file, dst + '/' + file, xor_code)
    pass


if __name__ == '__main__':
    main(input('src: '), input('dst: '))
    pass
