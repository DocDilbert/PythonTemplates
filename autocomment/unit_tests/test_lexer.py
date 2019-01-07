import pytest
from pycpp.lexer import Lexer
from pycpp.code import Token


LEXER_TESTS = [
    {
        'description': "lexer_basic_1",
        'input': ' ',
        'output': [
            Token('WHITESPACE', ' ', 0)
        ]
    }, {
        'description': "lexer_basic_2",
        'input': '  ',
        'output': [
            Token('WHITESPACE', '  ', 0)
        ]
    }, {
        'description': "lexer_basic_3",
        'input': '// TEST',
        'output': [
            Token('COMMENT', '//', 0),
            Token('WHITESPACE', ' ', 2),
            Token('STRING', 'TEST', 3)
        ]
    }, {
        'description': "lexer_basic_4",
        'input': '{TEST}',
        'output': [
            Token('CB_BEGIN', '{', 0),
            Token('STRING', 'TEST', 1),
            Token('CB_END', '}', 5)
        ]
    }, {
        'description': "lexer_basic_5",
        'input': 'ab c de',
        'output': [
            Token('STRING', 'ab', 0),
            Token('WHITESPACE', ' ', 2),
            Token('STRING', 'c', 3),
            Token('WHITESPACE', ' ', 4),
            Token('STRING', 'de', 5),
        ]
    }, {
        'description': "lexer_basic_6",
        'input': '/*TEST*/',
        'output': [
            Token('COMMENT_BEGIN', '/*', 0),
            Token('STRING', 'TEST', 2),
            Token('COMMENT_END', '*/', 6)
        ]
    }, {
        'description': "lexer_basic_7",
        'input': 'erw = _abc',
        'output': [
            Token('STRING', 'erw', 0),
            Token('WHITESPACE', ' ', 3),
            Token('EQUALS', '=', 4),
            Token('WHITESPACE', ' ', 5),
            Token('STRING', '_abc', 6)
        ]
    }
]


@pytest.mark.parametrize("testdata", LEXER_TESTS)
def test_lex(testdata):
    lexer = Lexer()
    lexer.input(testdata['input'])

    output = list(lexer.tokens())

    assert len(output) == len(
        testdata['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, testdata['output']):
        assert element[0] == element[1], testdata['description']
