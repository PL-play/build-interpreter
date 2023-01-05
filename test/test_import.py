import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):

    def test1(self):
        eva = Eva()
        eva.eval_global(parse('''
            (import Math)
        '''))
        self.assertEqual(eva.eval_global(parse('''
            ((prop Math abs) (- 10))
        ''')), 10)
        self.assertEqual(eva.eval_global(parse('''
            ((prop Math square) (- 10))
        ''')), 100)
        self.assertEqual(eva.eval_global(parse('''
            (prop Math MAX_VALUE)
        ''')), 1000)
