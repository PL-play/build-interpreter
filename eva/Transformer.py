class Transformer:
    def trans_def_to_var_lambda(self, exp):
        _, name, params, body = exp
        # JIT-transpile to a variable declaration
        return ['var', name, ['lambda', params, body]]
