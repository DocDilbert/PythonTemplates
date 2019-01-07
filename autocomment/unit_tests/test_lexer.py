import unittest
from pycpp import lexer


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
                lexer.Token('WHITESPACE', ' ', 0 )
            ]
        },
        {'input' : '  ', 
            'output' : [
                lexer.Token('WHITESPACE', '  ', 0 )
            ]
        },
        {'input' : '// TEST', 
            'output' : [
                lexer.Token('COMMENT', '//', 0 ),
                lexer.Token('WHITESPACE', ' ', 2 ),
                lexer.Token('STRING', 'TEST', 3 )
            ]
        },
        {'input' : '{TEST}', 
            'output' : [
                lexer.Token('CB_BEGIN', '{', 0 ),
                lexer.Token('STRING', 'TEST', 1 ),
                lexer.Token('CB_END', '}', 5 )
            ]
        },

        {'input' : '/*TEST*/', 
            'output' : [
                lexer.Token('COMMENT_BEGIN', '/*', 0 ),
                lexer.Token('STRING', 'TEST', 2 ),
                lexer.Token('COMMENT_END', '*/', 6 )
            ]
        },
        {'input' : 'erw = _abc', 
            'output' : [
                lexer.Token('STRING','erw',0 ),
                lexer.Token('WHITESPACE', ' ', 3 ),
                lexer.Token('EQUALS','=', 4 ),
                lexer.Token('WHITESPACE', ' ', 5 ),
                lexer.Token('STRING','_abc',6 )
            ]
        }
    ]

if __name__ == '__main__':
    unittest.main()
