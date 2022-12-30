import unittest

from eva.Eva import Eva


class EvaTest(unittest.TestCase):
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