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
              (def onClick (callback)
                (begin
                  (var x 10)
                  (var y 20)
                  (callback (+ x y))
                ))
              (onClick (lambda (data) (* data 10)))
            )
        ''')), 300)

    def test2(self):
        """
        Immediately-Invoked lambda expression - IILEs
        :return:
        """
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
            ((lambda (x) (* x x)) 2)
        ''')), 4)

    def test3(self):
        """
        save lambda to variable
        :return:
        """
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
            (begin
              (var square (lambda (x) (* x x)))
              (square 2)
            )
        ''')), 4)
