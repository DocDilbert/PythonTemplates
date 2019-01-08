import pytest
from pycpp.blockfactory import BlockFactory
from pycpp.code import Token, TokenNewLine
from pycpp.code import Closure

BLOCK_FACTORY_TESTS = [
    {
        'description': "blockfactory_test_0",
        'input': [
            Token('CB_BEGIN', '{', 0),
            Token('CB_END', '}', 1)
        ],
        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 1),
                []
            )
        ]
    },
    {
        'description': "blockfactory_test_1",
        'input': [
            Token('CB_BEGIN', '{', 0),
            TokenNewLine(1),
            Token('CB_END', '}', 2)
        ],
        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 2),
                [
                    TokenNewLine(1)
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_2",
        'input': [
            Token('CB_BEGIN', '{', 0),
            Token('CB_BEGIN', '{', 1),
            Token('CB_END', '}', 2),
            Token('CB_END', '}', 3)
        ],
        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_3",
        'input': [
            Closure(
                [
                    Token('CB_BEGIN', '{', 0),
                    Token('CB_END', '}', 1)
                ]
            )
        ],
        'output': [
            Closure(
                [
                    Token('CB_BEGIN', '{', 0),
                    Token('CB_END', '}', 1)
                ]
            )
        ]
    },
    {
        'description': "blockfactory_test_4",
        'input': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ],
        'output': [
            Closure(
                Token('CB_BEGIN', '{', 0),
                Token('CB_END', '}', 3),
                [
                    Closure(
                        Token('CB_BEGIN', '{', 1),
                        Token('CB_END', '}', 2),
                        []
                    )
                ]
            )
        ]
    }]


@pytest.mark.parametrize("data", BLOCK_FACTORY_TESTS)
def test_blockfactory(data):
    blockfactory = BlockFactory()
    blockfactory.input(data['input'])

    output = blockfactory.tree()
    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
