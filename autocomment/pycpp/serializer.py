from pycpp.code import Block


def getTokenValue(tok):
    return tok.val

def getTokenType(tok):
    return tok.type

def getTokenSummary(tok):
    return '('+str(tok.pos)+')' +tok.type +'_'
 
class Serializer:
    def __init__(self):
        pass

    def toString(self, tokens, func_getTokenString = getTokenValue):
        output = ''
        for tok in tokens:
            if isinstance(tok, Block):
                output += func_getTokenString(tok.begin_del)
                output += self.toString(tok.content, func_getTokenString)
                output += func_getTokenString(tok.end_del)
            else:
                output += func_getTokenString(tok)

        return output
