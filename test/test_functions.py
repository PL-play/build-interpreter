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
                (def square (x)
                (* x x))
                (square 2)
            )
        ''')), 4)

    def test2(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                    (begin 
                        (def calc (x y)
                            (begin 
                                (var z 30)
                                (+ (* x y) z)
                            ))
                        (calc 10 20)
                    )
                ''')), 230)

    def test3(self):
        """
        var value = 100
        def calc(x,y){
            var z = x + y
            def inner(foo){
                return foo + z + value
            }
            return inner
        }
        var fn = calc(10,20)
        return fn(30)

        :return:
        """
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                    (begin 
                      (var value 100)
                      (def calc (x y)
                        (begin
                          (var z (+ x y))
                          
                          (def inner (foo)
                            (+ (+ foo z) value))
                          inner    
                      ))
                      (var fn (calc 10 20))  
                      (fn 30)
                    )
                ''')), 160)

    def test4(self):
        """
        Recursive function
        """
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                           (begin 
                             (def factorial (x)
                               (if (== x 1)
                                 1
                                (* x (factorial (- x 1)))
                             ))
                             
                             (factorial 5)
                           )
                       ''')), 120)
