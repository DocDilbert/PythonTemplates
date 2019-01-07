import unittest
from pycpp import lexer
from pycpp import token

class TestLexer(unittest.TestCase):

    def test_lex(self):
        lexer_ = lexer.Lexer()
        
        for test in self.lexer_basic:
            lexer_.input(test['input'])

            output = list(lexer_.tokens())

            self.assertEqual(len(output),len(test['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge")

            for element in zip(output, test['output']):
                self.assertEqual(element[0], element[1])

    lexer_basic =   [
        {'input' : ' ', 
            'output' : [
                token.Token('WHITESPACE', ' ', 0 )
            ]
        },
        {'input' : '  ', 
            'output' : [
                token.Token('WHITESPACE', '  ', 0 )
            ]
        },
        {'input' : '// TEST', 
            'output' : [
                token.Token('COMMENT', '//', 0 ),
                token.Token('WHITESPACE', ' ', 2 ),
                token.Token('STRING', 'TEST', 3 )
            ]
        },
        {'input' : '{TEST}', 
            'output' : [
                token.Token('CB_BEGIN', '{', 0 ),
                token.Token('STRING', 'TEST', 1 ),
                token.Token('CB_END', '}', 5 )
            ]
        },

        {'input' : '/*TEST*/', 
            'output' : [
                token.Token('COMMENT_BEGIN', '/*', 0 ),
                token.Token('STRING', 'TEST', 2 ),
                token.Token('COMMENT_END', '*/', 6 )
            ]
        },
        {'input' : 'erw = _abc', 
            'output' : [
                token.Token('STRING','erw',0 ),
                token.Token('WHITESPACE', ' ', 3 ),
                token.Token('EQUALS','=', 4 ),
                token.Token('WHITESPACE', ' ', 5 ),
                token.Token('STRING','_abc',6 )
            ]
        }
    ]

if __name__ == '__main__':
    unittest.main()
