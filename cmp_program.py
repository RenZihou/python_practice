# -*- encoding: utf-8 -*-
# @Author: RZH

from random import choice, randint
from sys import stdout
from subprocess import Popen, PIPE


def gen_data() -> None:
    """
    generate input data
    """
    # a sample:
    n = randint(2, 10)
    with open('testcase.in', 'w', encoding='utf-8') as f:
        # please write your input data into the file `./testcase.in`
        f.write('%d\n' % n)
        for _ in range(n):
            f.write('%d ' % randint(1, 10))
    return


def compare(std: str, cmp: str) -> bool:
    """
    compare program `std` and `cmp` through auto generated input
    :param std: name of the program that return the correct answer
    :param cmp: name of the program that has bugs
    :return: True if the two programs reached a same answer, False otherwise
    """
    answer = Popen(
        std,
        stdin=open('testcase.in', 'r', encoding='utf-8'),
        stdout=PIPE
    ).stdout.readlines()
    out = Popen(
        cmp,
        stdin=open('testcase.in', 'r', encoding='utf-8'),
        stdout=PIPE
    ).stdout.readlines()
    answer = ''.join(map(bytes.decode, answer)).strip()
    out = ''.join(map(bytes.decode, out)).strip()
    if answer != out:
        print('\n=====INPUT=====\n%s\n'
              % ''.join(open('testcase.in', 'r', encoding='utf-8').readlines())
              )
        print('=====ANSWER====\n%s\n' % answer)
        print('=====OUTPUT====\n%s\n' % out)
        return False
    return True


if __name__ == '__main__':
    gen_data()
    count = 1
    std_ = 'CORRECT PROGRAM NAME'
    cmp_ = 'WRONG PROGRAM NAME'
    while compare(std=std_, cmp=cmp_):
        gen_data()
        stdout.write('\rtested %d cases.' % count)
        stdout.flush()
        count += 1
