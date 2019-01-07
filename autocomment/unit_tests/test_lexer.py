import unittest
from pycpp import lexer
from pycpp.code import Token

class TestLexer(unittest.TestCase):

    def test_lex(self):
        lexer_ = lexer.Lexer()

        for test in self.lexer_basic:
            lexer_.input(test['input'])

            output = list(lexer_.tokens())

            self.assertEqual(len(output),len(test['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge")

            for element in zip(output, test['output']):
                self.assertEqual(element[0], element[1])

    lexer_basic = [
        {'input' : ' ',
         'output' : [
             Token('WHITESPACE', ' ', 0)
         ]
        },
        {'input' : '  ',
         'output' : [
             Token('WHITESPACE', '  ', 0)
         ]
        },
        {'input' : '// TEST',
            'output' : [
                Token('COMMENT', '//', 0),
                Token('WHITESPACE', ' ', 2),
                Token('STRING', 'TEST', 3)
            ]
        },
        {'input' : '{TEST}',
            'output' : [
                Token('CB_BEGIN', '{', 0),
                Token('STRING', 'TEST', 1),
                Token('CB_END', '}', 5)
            ]
        },
        {'input' : 'ab c de',
            'output' : [
                Token('STRING', 'ab', 0),
                Token('WHITESPACE', ' ', 2),
                Token('STRING', 'c', 3),
                Token('WHITESPACE', ' ', 4),
                Token('STRING', 'de', 5),
            ]
        },
        {'input' : '/*TEST*/',
            'output' : [
                Token('COMMENT_BEGIN', '/*', 0),
                Token('STRING', 'TEST', 2),
                Token('COMMENT_END', '*/', 6)
            ]
        },
        {'input' : 'erw = _abc',
            'output' : [
                Token('STRING','erw',0),
                Token('WHITESPACE', ' ', 3),
                Token('EQUALS','=', 4),
                Token('WHITESPACE', ' ', 5),
                Token('STRING','_abc',6)
            ]
        }
    ]

if __name__ == '__main__':
    unittest.main()
