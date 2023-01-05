import numbers
import re
import types

from eva.Environment import Environment
from eva.Transformer import Transformer


class Eva:
    def __init__(self, global_env=Environment.global_env()):
        self.global_env = global_env
        self._transformer = Transformer()

    def eval_global(self, exp):
        return self._eval_body(exp, self.global_env)

    def eval(self, exp, env=None):
        print(f'start eval {exp}')
        if not env:
            env = self.global_env

        if self.is_number(exp):
            return exp

        if self.is_string(exp):
            return exp[1:-1]

        # if condition (if <condition> <consequent> <alternate>)
        if exp[0] == 'if':
            _, condition, consequent, alternate = exp
            return self.eval(consequent, env) if self.eval(condition, env) else self.eval(alternate, env)

        if exp[0] == 'switch':
            if_expression = self._transformer.trans_switch_to_if(exp)
            return self.eval(if_expression, env)
        # while
        if exp[0] == 'while':
            _, condition, body = exp
            result = None
            while self.eval(condition, env):
                result = self.eval(body, env)
            return result

        if exp[0] == 'for':
            while_exp = self._transformer.trans_for_to_while(exp)
            return self.eval(while_exp, env)

        # variables declaration : (var foo 1)
        if exp[0] == 'var':
            _, name, value = exp
            return env.define(name, self.eval(value, env))

        # variables update : (set foo 10)
        if exp[0] == 'set':
            _, ref, value = exp
            if not isinstance(ref, str) and ref[0] == 'prop':
                _, instance_name, prop_name = ref
                instance_env = self.eval(instance_name, env)
                return instance_env.define(prop_name, self.eval(value, env))
            return env.assign(ref, self.eval(value, env))

        # blocks
        if exp[0] == 'begin':
            block_env = Environment({}, env)
            # self.global_env = block_env
            return self._eval_block(exp, block_env)
        # blocks
        if exp[0] == 'block':
            # evaluate in the global environment
            return self._eval_block(exp, self.global_env)

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
        # Class declaration:(class <name> <parent> <body>)
        # A Class is an environment!!! -- a storage of methods and shared properties
        if exp[0] == 'class':
            _, name, parent, body = exp
            parent_env = self.eval(parent, env)
            parent_env = parent_env if parent_env else env
            class_env = Environment({}, parent_env)
            self._eval_body(body, class_env)
            print(f'create class {name}')
            return env.define(name, class_env)

        # Class instantiation: (new <class> <arguments>)
        # An instance of a Class is an environment!!!
        # its parent component of the instance environment is set to its class.
        if exp[0] == 'new':
            class_env = self.eval(exp[1], env)
            args = [self.eval(a, env) for a in exp[2:]]
            instance_env = Environment({}, class_env)
            # the first argument is 'this'
            self._user_defined_function(class_env.lookup('constructor'), [instance_env, *args])
            return instance_env

        # property access:(prop <instance> <name>)
        if exp[0] == 'prop':
            _, instance, name = exp
            instance_env = self.eval(instance, env)
            return instance_env.lookup(name)

        # super: (super <ClassName>)
        if exp[0] == 'super':
            _, class_name = exp
            return self.eval(class_name, env).get_parent()

        # module: (module <Name> <body>)
        if exp[0] == 'module':
            _, name, body = exp
            module_env = Environment({}, env)
            self._eval_body(body, module_env)
            return env.define(name, module_env)

        if self.is_varname(exp):
            return env.lookup(exp)

        if exp[0] == '++':
            pp_exp = self._transformer.trans_pp(exp)
            return self.eval(pp_exp, env)

        if exp[0] == '--':
            mm_exp = self._transformer.trans_mm(exp)
            return self.eval(mm_exp, env)

        if exp[0] == '+=':
            pe_exp = self._transformer.trans_pe(exp)
            return self.eval(pe_exp, env)

        if exp[0] == '-=':
            me_exp = self._transformer.trans_me(exp)
            return self.eval(me_exp, env)

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
                return self._user_defined_function(fn, args)

        raise NotImplementedError(f'{exp} not implemented!')

    def _user_defined_function(self, fn, args):
        activation_record = {}
        for index, item in enumerate(fn.get('params')):
            activation_record[item] = args[index]
        activation_env = Environment(activation_record,
                                     fn.get('env')  # static scope. dynamic scope if set to 'env'
                                     )
        return self._eval_body(fn.get('body'), activation_env)

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
