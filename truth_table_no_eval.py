# -*- encoding: utf-8 -*-
# @Author: RZH

"""
A simple program to print the truth table of a given formula
*no `eval()` or `exec()` function version*

Guides:
- input variables as uppercase letter (A, B, C, ..., Z)
- input True or False as `1` or `0`
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

from re import search, findall


class Statement(int):
    """
    redefine `>` `~` `==` operators of `int`
    """
    def __gt__(self, other):  # `>` means `implication` now
        return Statement(not self or other)

    def __invert__(self):
        return Statement(1 - self)

    def __eq__(self, other):
        return Statement(not (self - other))


class Formula(object):
    def __init__(self, formula: str):
        self.formula = formula.replace(' ', '')  # the given formula
        self.tmp_formula = self.formula
        # changes while calculating the value under a given situation
        self.variables = sorted(set(findall(r'[A-Z]', self.formula)))
        # variables such as `A`, `B`, ...

    def update(self):
        """
        update `self.tmp_formula` to handle another situation
        :return: self
        """
        self.tmp_formula = self.formula
        return self

    def eval(self, statements: dict) -> str:
        """
        calculate the truth value of `self.formula` under the given `statements`
        :param statements: the given statements
        :return: '0' or '1'
        """
        statements['0'] = Statement(0)
        statements['1'] = Statement(1)
        sub_formula = set(findall(r'\([A-Z01~&|^>=]+\)', self.tmp_formula))
        if sub_formula:
            for each in sub_formula:
                self.tmp_formula = self.tmp_formula.replace(
                    each, Formula(each.strip('()')).eval(statements)
                )
            return self.eval(statements)
        else:
            # calculate `~` first
            while True:
                # do loop until there is no `~` to handle `~~A` situation
                not_: list = findall(r'~[A-Z01]', self.tmp_formula)
                if not_:
                    for each in not_:
                        self.tmp_formula = self.tmp_formula.replace(
                            each, str(~statements[each[1]])
                        )
                else:
                    break

            # calculate `&` `|` `^` then
            while True:
                # do loop until there is no `&` to handle `A&B&C` situation
                and_ = search(r'[A-Z01]&[A-Z01]', self.tmp_formula)
                if and_:
                    and_ = str(and_.group())
                    self.tmp_formula = self.tmp_formula.replace(
                        and_, str(statements[and_[0]] & statements[and_[2]])
                    )
                else:
                    break
            while True:
                # do loop until there is no `|` to handle `A|B|C` situation
                or_ = search(r'[A-Z01]\|[A-Z01]', self.tmp_formula)
                if or_:
                    or_ = str(or_.group())
                    self.tmp_formula = self.tmp_formula.replace(
                        or_, str(statements[or_[0]] | statements[or_[2]])
                    )
                else:
                    break
            while True:
                # do loop until there is no `^` to handle `A^B^C` situation
                xor_ = search(r'[A-Z01]\^[A-Z01]', self.tmp_formula)
                if xor_:
                    xor_ = str(xor_.group())
                    self.tmp_formula = self.tmp_formula.replace(
                        xor_, str(statements[xor_[0]] ^ statements[xor_[2]])
                    )
                else:
                    break

            # calculate `>` `=` finally
            while True:
                # do loop until there is no `>` to handle `A>B>C` situation
                imp_ = search(r'[A-Z01]>[A-Z01]', self.tmp_formula)
                if imp_:
                    imp_ = str(imp_.group())
                    self.tmp_formula = self.tmp_formula.replace(
                        imp_, str(statements[imp_[0]] > statements[imp_[2]])
                    )
                else:
                    break
            while True:
                # do loop until there is no `=` to handle `A=B=C` situation
                eq_ = search(r'[A-Z01]=[A-Z01]', self.tmp_formula)
                if eq_:
                    eq_ = str(eq_.group())
                    self.tmp_formula = self.tmp_formula.replace(
                        eq_, str(statements[eq_[0]] == statements[eq_[2]])
                    )
                else:
                    break

            return self.tmp_formula

    def truth_table(self) -> None:
        """
        print the truth table
        :return: None
        """
        print('%s Ans' % ' '.join(self.variables))
        n = len(self.variables)
        for i in range(2 ** n):
            values: str = bin(i)[2:].rjust(n, '0')
            statements: dict = dict(
                zip(self.variables, map(Statement, map(int, values)))
            )
            # the values of statements will be stored in the dict `statements`
            result: str = self.update().eval(statements)
            print('%s  %s' % (values.replace('', ' ').strip(), result))
        return


if __name__ == '__main__':
    f = Formula(input())
    f.truth_table()
