class Environment:
    def __init__(self, record=None):
        if record is None:
            record = {}
        self._record = record

    def define(self, name, value):
        self._record[name] = value
        return value

    def lookup(self, name):
        value = self._record.get(name)
        if not value:
            raise ReferenceError(f'Variable {name} is not defined')
        return value
