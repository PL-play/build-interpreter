import numbers
import re

from eva.Environment import Environment


class Eva:
    def __init__(self, global_env=Environment()):
        self.global_env = global_env

    def eval(self, exp, env=None):
        if not env:
            env = self.global_env

        if self.is_number(exp):
            return exp

        if self.is_string(exp):
            return exp[1:-1]
        # comparison
        if exp[0] == '>':
            return self.eval(exp[1], env) > self.eval(exp[2], env)

        if exp[0] == '>=':
            return self.eval(exp[1], env) >= self.eval(exp[2], env)

        if exp[0] == '<':
            return self.eval(exp[1], env) < self.eval(exp[2], env)

        if exp[0] == '<=':
            return self.eval(exp[1], env) <= self.eval(exp[2], env)

        if exp[0] == '==':
            return self.eval(exp[1], env) == self.eval(exp[2], env)

        # if condition
        if exp[0] == 'if':
            _, condition, consequent, alternate = exp
            return self.eval(consequent, env) if self.eval(condition, env) else self.eval(alternate, env)

        # math
        if exp[0] == '+':
            return self.eval(exp[1], env) + self.eval(exp[2], env)

        if exp[0] == '-':
            return self.eval(exp[1], env) - self.eval(exp[2], env)

        if exp[0] == '*':
            return self.eval(exp[1], env) * self.eval(exp[2], env)

        if exp[0] == '/':
            return self.eval(exp[1], env) / self.eval(exp[2], env)

        # variables declaration : (var foo 1)
        if exp[0] == 'var':
            _, name, value = exp
            return env.define(name, self.eval(value, env))

        # variables update : (set foo 10)
        if exp[0] == 'set':
            _, name, value = exp
            return env.assign(name, value)

        if self.is_varname(exp):
            return env.lookup(exp)

        # blocks
        if exp[0] == 'begin':
            block_env = Environment({}, env)
            return self._eval_block(exp, block_env)

        raise NotImplementedError(f'{exp} not implemented!')

    def is_number(self, exp):
        return isinstance(exp, numbers.Number)

    def is_string(self, exp):
        return type(exp) == str and exp[0] == '"' and exp[-1] == '"'

    def is_varname(self, exp):
        return type(exp) == str and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', exp)

    def _eval_block(self, exp, env):
        return [self.eval(e, env) for e in exp[1:]][-1]
