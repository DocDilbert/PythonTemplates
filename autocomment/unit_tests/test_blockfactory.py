import pytest
from pycpp.blockfactory import BlockFactory
from pycpp.code import Token, TokenNewLine
from pycpp.code import Block

BLOCK_FACTORY_TESTS = [
    {
        'description': "blockfactory_test_0",
        'search_pattern': ('BEGIN','END'),
        'input': [
            Token('BEGIN', '{', 0),
            Token('END', '}', 1)
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 1),
                []
            )
        ]
    },
    {
        'description': "blockfactory_test_1",
        'search_pattern': ('BEGIN','END'),
        'input': [
            Token('BEGIN', '{', 0),
            TokenNewLine(1),
            Token('END', '}', 2)
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 2),
                [
                    TokenNewLine(1)
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_2",
        'search_pattern': ('BEGIN','END'),
        'input': [
            Token('BEGIN', '{', 0),
            Token('BEGIN', '{', 1),
            Token('END', '}', 2),
            Token('END', '}', 3)
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 3),
                [
                    Block(
                        Token('BEGIN', '{', 1),
                        Token('END', '}', 2),
                        []
                    )
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_3",
        'search_pattern': ('BEGIN','END'),
        'input': [
            Block(
                [
                    Token('BEGIN', '{', 0),
                    Token('END', '}', 1)
                ]
            )
        ],
        'output': [
            Block(
                [
                    Token('BEGIN', '{', 0),
                    Token('END', '}', 1)
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_4",
        'search_pattern': ('BEGIN','END'),
        'input': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 3),
                [
                    Block(
                        Token('BEGIN', '{', 1),
                        Token('END', '}', 2),
                        []
                    )
                ]
            )
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 3),
                [
                    Block(
                        Token('BEGIN', '{', 1),
                        Token('END', '}', 2),
                        []
                    )
                ]
            )
        ]
    }, 
    {
        'description': "blockfactory_test_5",
        'search_pattern': ('DOXYGENCOMMENT','NL'),
        'input': [
            Token('DOXYGENCOMMENT', '///', 0),
            TokenNewLine( 1)
        ],
        'output': [
            Block(
                Token('DOXYGENCOMMENT', '///', 0),
                TokenNewLine( 1),
                []
            )
        ]
    },
    {
        'description': "blockfactory_test_6",
        'search_pattern': ('DOXYGENCOMMENT','NL'),
        'input': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 3),
                [
                    Token('DOXYGENCOMMENT', '///', 1),
                    TokenNewLine(2),
                ]
            )
        ],
        'output': [
            Block(
                Token('BEGIN', '{', 0),
                Token('END', '}', 3),
                [
                    Block(
                        Token('DOXYGENCOMMENT', '///', 1),
                        TokenNewLine(2),
                        []
                    )
                ]
            )
        ]
    }, 
    {
        'description': "blockfactory_test_7",
        'search_pattern': ('DOXYGENCOMMENT','NL'),
        'input': [
            Token('DOXYGENCOMMENT', '///', 0),
            TokenNewLine(1),
            TokenNewLine(2)
        ],
        'output': [
            Block(
                Token('DOXYGENCOMMENT', '///', 0),
                TokenNewLine(1),
                [ ]
            ),
            TokenNewLine(2)
        ]
    },
]


@pytest.mark.parametrize("data", BLOCK_FACTORY_TESTS)
def test_blockfactory(data):
    search_pattern = data['search_pattern']
    blockfactory = BlockFactory(begin_token_type=search_pattern[0], end_token_type=search_pattern[1])
    blockfactory.input(data['input'])

    output = blockfactory.tree()
    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
