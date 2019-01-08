from pycpp.code import Token
from pycpp.code import Closure


class BlockFactory(object):
    def __init__(self):
        self.tokens = []

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
                if token.type == "CB_BEGIN":
                    temp = Closure()
                    temp.begin_del = token
                    closure_tree.append(actual)
                    actual.add(temp)
                    actual = temp
                elif token.type == "CB_END":
                    actual.end_del = token
                    actual = closure_tree.pop()
                else:
                    actual.add(token)

        return output.content

    def tree(self):
        return self.tree_recursive(self.tokens)
