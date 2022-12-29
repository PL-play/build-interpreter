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
