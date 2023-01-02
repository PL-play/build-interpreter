import numbers
import re
import types

from eva.Environment import Environment
from eva.Transformer import Transformer


class Eva:
    def __init__(self, global_env=Environment.global_env()):
        self.global_env = global_env
        self._transformer = Transformer()

    def eval(self, exp, env=None):
        print(f'start eval {exp}')
        if not env:
            env = self.global_env

        if self.is_number(exp):
            return exp

        if self.is_string(exp):
            return exp[1:-1]

        if self.is_varname(exp):
            return env.lookup(exp)

        # if condition
        if exp[0] == 'if':
            _, condition, consequent, alternate = exp
            return self.eval(consequent, env) if self.eval(condition, env) else self.eval(alternate, env)
        # while
        if exp[0] == 'while':
            _, condition, body = exp
            result = None
            while self.eval(condition, env):
                result = self.eval(body, env)
            return result

        # variables declaration : (var foo 1)
        if exp[0] == 'var':
            _, name, value = exp
            return env.define(name, self.eval(value, env))

        # variables update : (set foo 10)
        if exp[0] == 'set':
            _, name, value = exp
            return env.assign(name, self.eval(value, env))

        # blocks
        if exp[0] == 'begin':
            block_env = Environment({}, env)
            return self._eval_block(exp, block_env)

        # function declaration: (def foo (x) (* x x))
        """
        _, name, params, body = exp
            fn = {
                'params': params,
                'body': body,
                'env': env  # closure
            }
            return env.define(name, fn)
        """
        # Syntactic sugar for: (var foo (lambda (x) (* x x)))
        if exp[0] == 'def':
            _, name, params, body = exp
            # JIT-transpile to a variable declaration
            var_expression = self._transformer.trans_def_to_var_lambda(exp)
            return self.eval(var_expression, env)

        # lambda function declaration: (lambda (x) (* x x))
        if exp[0] == 'lambda':
            _, params, body = exp
            return {
                'params': params,
                'body': body,
                'env': env  # closure
            }

        # function call
        if isinstance(exp, list) or isinstance(exp, tuple):
            print(f'-- function call {exp}')
            fn = self.eval(exp[0], env)
            args = [self.eval(e, env) for e in exp[1:]]
            # build-in functions
            if isinstance(fn, types.FunctionType) or \
                    isinstance(fn, types.BuiltinFunctionType) or \
                    isinstance(fn, types.MethodType):
                value = fn(*args)
                print(f'--- call built-in function {fn} ({args}), result {value}')
                return value
            else:
                # user defined functions
                # function call in a new environment
                # 1. install past arguments to the parameters
                print(f'--- call user defined function  {exp[0]} ({args})')
                activation_record = {}
                for index, item in enumerate(fn.get('params')):
                    activation_record[item] = args[index]
                activation_env = Environment(activation_record,
                                             fn.get('env')  # static scope. dynamic scope if set to 'env'
                                             )
                return self._eval_body(fn.get('body'), activation_env)

        raise NotImplementedError(f'{exp} not implemented!')

    def is_number(self, exp):
        return isinstance(exp, numbers.Number)

    def is_string(self, exp):
        return type(exp) == str and exp[0] == '"' and exp[-1] == '"'

    def is_varname(self, exp):
        return type(exp) == str and re.match(r'^[+\-*/><=a-zA-Z0-9_]+$', exp)

    def _eval_block(self, exp, env):
        expressions = exp[1:]
        result = None
        for e in expressions:
            result = self.eval(e, env)
        return result

    def _eval_body(self, body, env):
        if body[0] == 'begin':
            return self._eval_block(body, env)
        return self.eval(body, env)
