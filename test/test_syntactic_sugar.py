import unittest

from eva.Eva import Eva
from util.Parser import parse


class EvaTest(unittest.TestCase):

    def test1(self):
        """
        for -> while

        (for <init>
            <condition>
            <modifier>
            <exp>)

        (begin
          <init>
          while <condition>
            (begin
              <exp>
              <modifier>
            )
        )
        :return:
        """
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                                 ( begin
                                   (var result 0)
                                   (for (var i 0) (< i 10) (set i (+ i 1))
                                      (begin
                                        (set result (+ result 1))
                                      )
                                   )
        
                                 )
                              ''')), 10)

    def test2(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                                         (begin 
                                            (var i 1)
                                            (++ i)
                                         )
                                      ''')), 2)

    def test3(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                                            (begin 
                                               (var i 1)
                                               (-- i)
                                            )
                                         ''')), 0)

    def test4(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                                            (begin 
                                               (var i 1)
                                               (-= i 5)
                                            )
                                         ''')), -4)

    def test5(self):
        eva = Eva()
        self.assertEqual(eva.eval(parse('''
                                            (begin 
                                               (var i 1)
                                               (+= i 5)
                                            )
                                         ''')), 6)
