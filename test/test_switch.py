import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):
    """

    """

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                    (begin
                        (var x 10)
                        (switch 
                          ((== x 10) 100)
                          ((> x 10) 200)
                          (else 300)
                        )
                    )
                    
                ''')), 100)
