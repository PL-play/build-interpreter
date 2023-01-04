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
