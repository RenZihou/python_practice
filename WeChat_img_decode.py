# -*- coding: utf-8 -*-
# @Author: RZH

"""
Decrypt WeChat images in folder:
...\\WeChat Files\\WeChat_id\\FileStorage\\Image\\yyyy-mm

All image files have been encrypted with XOR operation, and
the number used for XOR operation by different clients is different
So we need to figure out the number first and then use it to
decrypt all the files.
"""

from os import listdir
from tqdm import tqdm

JPG_HEADER = (0xFF, 0xD8)  # .jpg files start with 0xFFD8
PNG_HEADER = (0x89, 0x50)  # .png files start with 0x8950


def get_xor_code(sample_file: str) -> int:
    """
    Figure out the number used to do XOR operation
    :param sample_file: a random file in the folder
    :return: the number
    """
    with open(sample_file, 'rb') as f:
        header = tuple(f.read(2))
    if header[0] ^ JPG_HEADER[0] == header[1] ^ JPG_HEADER[1]:
        return header[0] ^ JPG_HEADER[0]
    else:
        return header[0] ^ PNG_HEADER[0]


def decode_file(src_file: str, dst_file: str, xor_code: int) -> None:
    """
    Decrypt a single file
    :param src_file: the encrypted .dat file
    :param dst_file: the decrypted .jpg / .png file
    :param xor_code: the number used in XOR operation
    :return: None
    """
    new_byte = list()
    with open(src_file, 'rb') as f:
        for byte in f.read():
            new_byte.append(byte ^ xor_code)
    suffix = '.jpg' if new_byte[0] == JPG_HEADER[0] else '.png'
    with open(dst_file.replace('.dat', suffix), 'wb') as f:
        f.write(bytes(new_byte))
    return None


def main(src: str, dst: str) -> int:
    """
    Decrypt all the files in a folder
    :param src: the folder that stores the image files
    :param dst: the output folder
    :return: the count of files decrypted
    """
    files = list(filter(lambda x: x[-4:] == '.dat', listdir(src)))
    xor_code = get_xor_code(src + '/' + files[0])
    for file in tqdm(files):
        decode_file(src + '/' + file, dst + '/' + file, xor_code)
    return len(files)


if __name__ == '__main__':
    count = main(input('src: '), input('dst: '))
    print('Decrypted %d files successfully' % count)
    pass
