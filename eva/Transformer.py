class Transformer:
    def trans_def_to_var_lambda(self, exp):
        _, name, params, body = exp
        # JIT-transpile to a variable declaration
        return ['var', name, ['lambda', params, body]]

    def trans_switch_to_if(self, exp):
        # (switch (case1) (case2) ..)
        cases = exp[1:]
        if_exp = ['if', None, None, None]
        current = if_exp
        for i in range(0, len(cases) - 1):
            current_cond, current_block = cases[i]
            current[1] = current_cond
            current[2] = current_block
            next = cases[i + 1]
            next_cond, next_block = next
            current[3] = next_block if next_cond == 'else' else ['if', None, None, None]
            current = current[3]
        return if_exp

    def trans_for_to_while(self, exp):
        """
         for -> while

        (for <init>
            <condition>
            <modifier>
            <exp>)

        (begin
          <init>
          while <condition>
            (begin
              <exp>
              <modifier>
            )
        )
        :param exp:
        :return:
        """

        _, init, condition, modifier, for_exp = exp
        while_exp = ['begin', init, ['while', condition, ['begin', for_exp, modifier]]]
        return while_exp
