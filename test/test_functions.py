import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):
    """
    (if <condition>
        <consequent>
        <alternate>
    )
    """

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
            (begin 
                (def square (x)
                (* x x))
                (square 2)
            )
        ''')), 4)
