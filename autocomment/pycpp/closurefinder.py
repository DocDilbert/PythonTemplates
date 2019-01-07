from pycpp.token import Token
from pycpp.token import Closure

class ClosureFinder(object):
    def __init__(self):
        pass

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
                actual=temp

            actual.add(token)

            if token.type == "CB_END":
                actual = closure_tree.pop()
        
        return(output.content)