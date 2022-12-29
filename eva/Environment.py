class Environment:
    def __init__(self, record=None):
        if record is None:
            record = {}
        self._record = record

    def define(self, name, value):
        self._record[name] = value
        return value

    def lookup(self, name):
        if not self._record.__contains__(name):
            raise ReferenceError(f'Variable {name} is not defined')
        return self._record[name]
