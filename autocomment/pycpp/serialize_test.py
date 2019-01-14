from pycpp.lexer import Lexer
from pycpp.serializer import Serializer, getTokenSummary
from pycpp.blockfactory import BlockFactory

if __name__ == "__main__":

    inp = ''' 
        // testMethod
        void testMethod(Namespace::A1 a1)
        {
          Code
        }
        '''
    lexer = Lexer()
    lexer.input(inp)
    i1 = list(lexer.tokens())

    cb_factory = BlockFactory()
    i2 = cb_factory.tree(i1)

    serializer = Serializer()

    buf = serializer.toString(i2, getTokenSummary)

    print(buf)
