import pytest
from pycpp.lexer import Lexer
from pycpp.code import Token, TokenNewLine


LEXER_TESTS = [
    {
        'description': "lexer_test_1",
        'input': ' ',
        'output': [
            Token('WS', ' ', 0)
        ]
    }, {
        'description': "lexer_test_2",
        'input': '  ',
        'output': [
            Token('WS', '  ', 0)
        ]
    }, {
        'description': "lexer_test_3",
        'input': '// TEST',
        'output': [
            Token('COMMENT', '//', 0),
            Token('WS', ' ', 2),
            Token('STRING', 'TEST', 3)
        ]
    }, {
        'description': "lexer_test_4",
        'input': '{TEST}',
        'output': [
            Token('CB_BEGIN', '{', 0),
            Token('STRING', 'TEST', 1),
            Token('CB_END', '}', 5)
        ]
    }, {
        'description': "lexer_test_5",
        'input': 'ab c de',
        'output': [
            Token('STRING', 'ab', 0),
            Token('WS', ' ', 2),
            Token('STRING', 'c', 3),
            Token('WS', ' ', 4),
            Token('STRING', 'de', 5),
        ]
    }, {
        'description': "lexer_test_6",
        'input': '/*TEST*/',
        'output': [
            Token('COMMENT_BEGIN', '/*', 0),
            Token('STRING', 'TEST', 2),
            Token('COMMENT_END', '*/', 6)
        ]
    }, {
        'description': "lexer_test_7",
        'input': 'erw = _abc',
        'output': [
            Token('STRING', 'erw', 0),
            Token('WS', ' ', 3),
            Token('EQUALS', '=', 4),
            Token('WS', ' ', 5),
            Token('STRING', '_abc', 6)
        ]
    }, {
        'description': "lexer_test_8",
        'input': ' \n ',
        'output': [
            Token('WS', ' ', 0),
            TokenNewLine(1),
            Token('WS', ' ', 2)
        ]
    }, {
        'description': "lexer_test_9",
        'input': '\n\n\n',
        'output': [
            TokenNewLine(0),
            TokenNewLine(1),
            TokenNewLine(2),
        ]
    },
]


@pytest.mark.parametrize("data", LEXER_TESTS)
def test_lex(data):
    lexer = Lexer()
    lexer.input(data['input'])

    output = list(lexer.tokens())

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
