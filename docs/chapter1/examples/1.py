import os
import sys


class TestPython(object):
    def __init__(self, a: str = '1'):
        self.a = a

    def avalue(self):
        return self.a

    @property
    def pvalue(self):
        return self.a


if __name__ == "__main__":
    tp = TestPython(a = '2')
    print(tp.avalue())
    print(tp.pvalue)
    print(os.listdir('./'))