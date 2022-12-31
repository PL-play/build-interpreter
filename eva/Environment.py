class Environment:
    def __init__(self, record=None, parent=None):
        if record is None:
            record = {}
        self._record = record
        self._parent = parent

    def define(self, name, value):
        self._record[name] = value
        return value

    def assign(self, name, value):
        self.resolve(name)._record[name] = value
        return value

    def lookup(self, name):
        return self.resolve(name)._record[name]

    def resolve(self, name):
        if self._record.__contains__(name):
            return self
        if self._parent is None:
            raise ReferenceError(f'Variable {name} is not defined')
        return self._parent.resolve(name)

    @staticmethod
    def global_env():
        def plus(op1, op2):
            return op1 + op2

        def minus(op1, op2):
            if op2 is None:
                return -op1
            return op1 - op2

        def multiply(op1, op2):
            return op1 * op2

        def divide(op1, op2):
            return op1 / op2

        def gt(op1, op2):
            return op1 > op2

        def ge(op1, op2):
            return op1 >= op2

        def lt(op1, op2):
            return op1 < op2

        def le(op1, op2):
            return op1 <= op2

        def eq(op1, op2):
            return op1 == op2

        return Environment({
            'true': True,
            'false': False,
            'null': None,
            '+': plus,
            '-': minus,
            '*': multiply,
            '/': divide,
            '>': gt,
            '>=': ge,
            '<': lt,
            '<=': le,
            '==': eq

        })
