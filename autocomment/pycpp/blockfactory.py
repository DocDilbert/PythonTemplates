from pycpp.code import Token
from pycpp.code import Closure


class BlockFactory(object):
    def __init__(self,*, begin_token_type="BEGIN", end_token_type="END"):
        self.tokens = []
        self.begin_token_type = begin_token_type
        self.end_token_type = end_token_type

    def input(self, tokens):
        self.tokens = tokens

    def tree_recursive(self, tokens):
        output = Closure()
        actual = output
        closure_tree = []

        for token in tokens:
            if isinstance(token, Closure):
                output.add(Closure(token.begin_del, token.end_del,
                                   self.tree_recursive(token.content)))
            else:
                if token.type == self.begin_token_type:
                    temp = Closure()
                    temp.begin_del = token
                    closure_tree.append(actual)
                    actual.add(temp)
                    actual = temp
                # do not use end tokens which have no corresponding begin token
                elif token.type == self.end_token_type and len(closure_tree)>0:
                    actual.end_del = token
                    actual = closure_tree.pop()
                else:
                    actual.add(token)

        return output.content

    def tree(self):
        return self.tree_recursive(self.tokens)
