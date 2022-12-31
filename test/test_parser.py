import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):
    def test3(self):
        eva = Eva()

        self.assertEqual(eva.eval(parse('''
            (begin 
                (var x 10)
                (var y 20)
                (+ (* x 10) y)
            )
        ''')), 120)
