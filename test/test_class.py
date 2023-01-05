import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
            (block 
              (class Point null
                (begin
                  (def constructor (this x y)
                    (begin
                      (set (prop this x) x)
                      (set (prop this y) y)
                    )
                  )
                  (def calc (this)
                    (+ (prop this x) (prop this y))
                  )
                )
              )
              (var p (new Point 10 20))
              ((prop p calc) p)
            )
        ''')), 30)
        self.assertEqual(eva.eval(parse('''
            (begin
              (var p2 (new Point 45 24))
              ((prop p2 calc) p2)
            )
        ''')), 69)
