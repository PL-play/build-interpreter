import unittest

from eva.Environment import Environment
from eva.Eva import Eva


class EvaTest(unittest.TestCase):
    """
    (while <condition>
        <block>
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

    def test2(self):
        eva = Eva()
        self.assertEqual(eva.eval(
            ['begin',
             ['var', 'result', 0],
             ['var', 'i', 0],
             ['while', ['<', 'i', 1],
              ['begin',
               ['set', 'result', ['+', 'result', 1]],
               ['set', 'i', ['+', 'i', 1]],
               ]
              ],
             'result'
             ]

        ), 1)
