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
        {'input' : 'erw = _abc', 
            'output' : [
                lexer.Token('IDENTIFIER','erw',0 ),
                lexer.Token('WHITESPACE', ' ', 3 ),
                lexer.Token('EQUALS','=', 4 ),
                lexer.Token('WHITESPACE', ' ', 5 ),
                lexer.Token('IDENTIFIER','_abc',6 )
            ]
        }
    ]

if __name__ == '__main__':
    unittest.main()
