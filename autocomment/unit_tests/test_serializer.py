import pytest
from pycpp.code import Token
from pycpp.code import Block
from pycpp.serializer import Serializer

TO_STRING_TESTS = [
    {
        'description': "test_serializer_0",
        'search_pattern': ('A', 'B'),
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
        'description': "test_serializer_1",
        'search_pattern': ('A', 'B'),
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
    }
]


@pytest.mark.parametrize("data", TO_STRING_TESTS)
def test_to_string(data):
    serializer = Serializer()
    output = list(serializer.toString(data['input']))

    assert len(output) == len(
        data['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, data['output']):
        assert element[0] == element[1], data['description']
