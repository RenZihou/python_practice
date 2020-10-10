# -*- encoding: utf-8 -*-
# @Author: RZH

"""
A simple program to print the truth table of a given formula

Guides:
- input variables as uppercase letter (A, B, C, ..., Z)
- input connectives as following:
    - `~`: not
    - `&`: and
    - `|`: or
    - `^`: xor
    - `>`: implication
    - `=`: double implication
- brackets (`(` and `)`) are supported
- spaces will be omitted

If the given formula is invalid, an exception will be raised
"""

from re import findall, sub


class Statement(int):
    def __gt__(self, other):  # >
        return Statement(not self or other)


class Formula(object):
    def __init__(self, formula):
        self.formula = formula.replace('=', '==')
        # we will need `==` instead of `=` to call the `__eq__` function

    def truth_table(self):
        """
        print the truth table
        :return: None
        """
        variables = sorted(set(findall(r'[A-Z]', self.formula)))
        print('%s Ans' % ' '.join(variables))
        n = len(variables)
        for i in range(2 ** n):
            values: str = bin(i)[2:].rjust(n, '0')
            statements: dict = dict(
                zip(variables, map(Statement, map(int, values)))
            )
            formula: str = sub(r'([A-Z])', r'statements["\1"]', self.formula)
            # the values of statements will be stored in the dict `statements`
            result: Statement = eval(formula)
            print('%s  %s' % (values.replace('', ' ').strip(), result))
        return


if __name__ == '__main__':
    f = Formula(input())
    f.truth_table()
