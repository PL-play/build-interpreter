import unittest

from eva.Eva import Eva


class EvaTest(unittest.TestCase):

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(10), 10)

    def test2(self):
        eva = Eva()
        self.assertEqual(eva.eval('"hello"'), 'hello')