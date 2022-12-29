import unittest

from eva.Environment import Environment
from eva.Eva import Eva


class EvaTest(unittest.TestCase):

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(10), 10)

    def test2(self):
        eva = Eva()
        self.assertEqual(eva.eval('"hello"'), 'hello')

    def test3(self):
        eva = Eva()
        self.assertEqual(eva.eval(('+', 1, 3)), 4)

    def test4(self):
        eva = Eva()
        self.assertEqual(eva.eval(('+', 3, 5)), 8)

    def test5(self):
        eva = Eva()
        self.assertEqual(eva.eval(('+', 3, ('+', 4, 6))), 13)

    def test6(self):
        eva = Eva()
        self.assertEqual(eva.eval(('-', 3, 3)), 0)

    def test7(self):
        eva = Eva()
        self.assertEqual(eva.eval(('-', 3, ('-', 6, 2))), -1)

    def test8(self):
        eva = Eva()
        self.assertEqual(eva.eval(('*', 2, 2)), 4)

    def test9(self):
        eva = Eva()
        self.assertEqual(eva.eval(('/', 6, 2)), 3)

    def test10(self):
        eva = Eva()
        self.assertEqual(eva.eval(('var', 'x', 2)), 2)

    def test11(self):
        eva = Eva()
        eva.eval(('var', 'x0', 2))
        self.assertEqual(eva.eval('x0'), 2)

    def test12(self):
        eva = Eva(Environment({
            'true': True,
            'false': False,
            'null': None
        }))
        self.assertEqual(eva.eval('true'), True)
        self.assertEqual(eva.eval('false'), False)
        self.assertEqual(eva.eval('null'), None)

    def test13(self):
        eva = Eva()
        self.assertEqual(eva.eval(('var', 'x', ('*', 2, 3))), 6)
        self.assertEqual(eva.eval('x'), 6)

    def test14(self):
        eva = Eva()
        self.assertEqual(eva.eval(['begin',
                                   ['var', 'x', 10],
                                   ['var', 'y', 20],
                                   ['+', 20, ['*', 'x', 'y']]]), 220)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(EvaTest())

    runner = unittest.TextTestRunner()
    runner.run(suite)
