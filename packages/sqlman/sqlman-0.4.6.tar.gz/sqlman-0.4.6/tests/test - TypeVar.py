# -*- coding: utf-8 -*-

from typing import TypeVar


class ASpider:
    def color(self):
        pass


class BSpider:
    def color(self):
        pass


class CSpider:
    def color(self):
        pass


Spider = TypeVar('Spider', ASpider, BSpider, CSpider)


def action(worker: Spider):
    print("传入了 ==> {}".format(worker))
    pass


action(6666)
action("200")
action(CSpider())

type2 = str | int
a = 200


def demo(t: type2):
    print(t)


if __name__ == '__main__':
    demo(200)
