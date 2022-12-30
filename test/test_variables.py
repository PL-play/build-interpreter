import unittest

from eva.Environment import Environment
from eva.Eva import Eva


class EvaTest(unittest.TestCase):

    def test10(self):
        eva = Eva()
        self.assertEqual(eva.eval(('var', 'x', 2)), 2)

    def test11(self):
        eva = Eva()
        eva.eval(('var', 'x0', 2))
        self.assertEqual(eva.eval('x0'), 2)

    def test12(self):
        eva = Eva(Environment({
            'true': True,
            'false': False,
            'null': None
        }))
        self.assertEqual(eva.eval('true'), True)
        self.assertEqual(eva.eval('false'), False)
        self.assertEqual(eva.eval('null'), None)

    def test13(self):
        eva = Eva()
        self.assertEqual(eva.eval(('var', 'x', ('*', 2, 3))), 6)
        self.assertEqual(eva.eval('x'), 6)

    def test14(self):
        eva = Eva()
        eva.eval(('var', 'x', 0))
        self.assertEqual(eva.eval(('set', 'x', ('*', 2, 3))), 6)
        self.assertEqual(eva.eval('x'), 6)
