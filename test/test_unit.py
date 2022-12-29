import unittest

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


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(EvaTest())

    runner = unittest.TextTestRunner()
    runner.run(suite)
