from pycpp.lexer import Lexer
from pycpp.serializer import Serializer, get_token_summary
from pycpp.blockfactory import BlockFactory

if __name__ == "__main__":
    inp = '''
        FLOAT32 method (enum argument name);
        '''
    lexer = Lexer()
    lexer.input(inp)
    i1 = list(lexer.tokens())

    cb_factory = BlockFactory()
    i2 = cb_factory.tree(i1)

    serializer = Serializer()

    buf = serializer.to_string(i2, get_token_summary)

    print(buf)
