import unittest

from eva.Environment import Environment
from eva.Eva import Eva


class EvaTest(unittest.TestCase):
    """
    (if <condition>
        <consequent>
        <alternate>
    )
    """

    def test1(self):
        eva = Eva()
        self.assertEqual(eva.eval(
            ['begin',
             ['var', 'counter', 0],
             ['var', 'result', 0],
             ['while', ['<', 'counter', 10],
              ['begin',
               # TODO implement '++'
               ['set', 'result', ['+', 'result', 1]],
               ['set', 'counter', ['+', 'counter', 1]],
               ],
              ],
             'result'
             ],
        ), 10)
