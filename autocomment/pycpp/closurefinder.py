from pycpp.code import Token
from pycpp.code import Closure


class ClosureFinder(object):
    def __init__(self):
        self.tokens = []

    def input(self, tokens):
        self.tokens = tokens

    
    def tree(self):
        output = Closure()
        actual = output
        closure_tree = []

        for token in self.tokens:
            if token.type == "CB_BEGIN":
                temp = Closure()
                closure_tree.append(actual)
                actual.add(temp)
                actual = temp

            actual.add(token)

            if token.type == "CB_END":
                actual = closure_tree.pop()

        return output.content
