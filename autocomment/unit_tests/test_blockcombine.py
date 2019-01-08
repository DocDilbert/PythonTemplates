import pytest
from pycpp.blockcombine import BlockCombine
from pycpp.code import Token, TokenNewLine
from pycpp.code import Block

BLOCK_COMBINE_TESTS = [
    {
        'description': "blockcombine_test_0",
        'search_pattern': ('BEGIN', 'END'),
        'input': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 5),
                [
                    Token('WHITESPACE', ' ', 1),
                    Token('WHITESPACE', ' ', 2),
                    Token('WHITESPACE', ' ', 3),
                    Token('WHITESPACE', ' ', 4),
                ]
            )
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 5),
                [
                    Token('STRING', '    ', 1),
                ]
            )
        ]
    }, {
        'description': "blockcombine_test_1",
        'search_pattern': ('DOXYGENCOMMENT', 'NL'),
        'input': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 7),
                [
                    Block(
                        Token('DOXYGENCOMMENT', '///', 1),
                        Token('NL', '\n', 6),
                        [
                            Token('WHITESPACE', ' ', 2),
                            Token('WHITESPACE', ' ', 3),
                            Token('WHITESPACE', ' ', 4),
                            Token('WHITESPACE', ' ', 5),
                        ]
                    )
                ]
            )
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 7),
                [
                    Block(
                        Token('DOXYGENCOMMENT', '///', 1),
                        Token('NL', '\n', 6),
                        [
                            Token('STRING',  '    ', 2),
                        ]
                    )
                ]
            )
        ]
    }, {
        'description': "blockcombine_test_2",
        'search_pattern': ('BEGIN', 'END'),
        'input': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 5),
                [
                ]
            )
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 5),
                [
                ]
            )
        ]
    },

]


@pytest.mark.parametrize("data", BLOCK_COMBINE_TESTS)
def test_blockcombine(data):
    search_pattern = data['search_pattern']
    blockcombine = BlockCombine(
        begin_token_type=search_pattern[0],
        end_token_type=search_pattern[1]
    )
    output = blockcombine.tree(data['input'])
    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
