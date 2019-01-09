import pytest
from pycpp.code import Token
from pycpp.code import Block
from pycpp.serializer import Serializer
from pycpp.serializer import getTokenType
from pycpp.serializer import getTokenValue
from pycpp.serializer import getTokenSummary
TO_STRING_TESTS = [
    {
        'description': "test_toString_0",
        'funcTokenString': getTokenValue,
        'input': [
            Token('A', 'a', 0),
            Token('B', 'b', 1),
            Token('C', 'c', 2),
            Token('D', 'd', 3),
            Token('E', 'e', 4)
        ],
        'output': 'abcde'
    },
    {
        'description': "test_toString_1",
        'funcTokenString': getTokenValue,
        'input': [
            Block(
                Token('A', 'a', 0),
                Token('E', 'e', 4),
                [
                    Token('B', 'b', 1),
                    Token('C', 'c', 2),
                    Token('D', 'd', 3),
                ]
            )
        ],
        'output': 'abcde'
    },
    {
        'description': "test_toString_2",
        'funcTokenString': getTokenType,
        'input': [
            Token('A', 'a', 0),
            Token('B', 'b', 1),
            Token('C', 'c', 2),
            Token('D', 'd', 3),
            Token('E', 'e', 4)
        ],
        'output': 'ABCDE'
    },
    {
        'description': "test_toString_3",
        'funcTokenString': getTokenSummary,
        'input': [
            Token('A', 'a', 0),
            Token('B', 'b', 1),
            Token('C', 'b', 2),
        ],
        'output': '(0)A_(1)B_(2)C_'
    },
]


@pytest.mark.parametrize("data", TO_STRING_TESTS)
def test_to_string(data):
    serializer = Serializer()
    output = list(serializer.toString(data['input'], data['funcTokenString']))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
