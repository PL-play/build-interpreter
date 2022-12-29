import numbers


class Eva:
    def __init__(self):
        self.global_env = None

    def eval(self, exp):
        if self.is_number(exp):
            return exp

        if self.is_string(exp):
            return exp[1:-1]

        if exp[0] == '+':
            return self.eval(exp[1]) + self.eval(exp[2])

        if exp[0] == '-':
            return self.eval(exp[1]) - self.eval(exp[2])

        if exp[0] == '*':
            return self.eval(exp[1]) * self.eval(exp[2])

        if exp[0] == '/':
            return self.eval(exp[1]) / self.eval(exp[2])

        raise NotImplementedError(f'{exp} not implemented!')

    def is_number(self, exp):
        return isinstance(exp, numbers.Number)

    def is_string(self, exp):
        return type(exp) == str and exp[0] == '"' and exp[-1] == '"'
