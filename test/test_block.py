import unittest

from eva.Eva import Eva


class EvaTest(unittest.TestCase):
    def test14(self):
        eva = Eva()
        self.assertEqual(eva.eval(['begin',
                                   ['var', 'x', 10],
                                   ['var', 'y', 20],
                                   ['+', 20, ['*', 'x', 'y']]]), 220)

    def test15(self):
        eva = Eva()
        self.assertEqual(eva.eval(['begin',
                                   ['var', 'x', 10],
                                   ['begin',
                                    ['var', 'x', 20],
                                    'x'
                                    ],
                                   'x'
                                   ]), 10)

    def test16(self):
        eva = Eva()
        self.assertEqual(eva.eval(['begin',
                                   ['var', 'value', 10],
                                   ['var', 'result', [
                                       'begin',
                                       ['var', 'x', ['+', 'value', 10]],
                                       'x'
                                   ]],
                                   'result'
                                   ]), 20)

    def test17(self):
        eva = Eva()
        self.assertEqual(eva.eval(['begin',
                                   ['var', 'value', 10],

                                   ['begin',
                                    ['set', 'value', 100],
                                    ],
                                   'value'
                                   ]), 100)