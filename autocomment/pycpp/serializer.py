from pycpp.code import Block


class Serializer:
    def __init__(self):
        pass

    def toString(self, tokens):
        output = ''
        for tok in tokens:
            if isinstance(tok, Block):
                output += tok.begin_del.val
                output += self.toString(tok.content)
                output += tok.end_del.val
            else:
                output += tok.val

        return output
