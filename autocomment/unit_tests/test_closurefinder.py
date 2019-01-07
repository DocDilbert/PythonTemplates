
import pytest
from pycpp.closurefinder import ClosureFinder
from pycpp.code import Token
from pycpp.code import Closure

CLOSURE_FINDER_TESTS = [
    {
        'description': "closure_finder_basic_1",
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
        'description': "closure_finder_basic_2",
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
        'description': "closure_finder_basic_3",
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
        'description': "closure_finder_basic_4",
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


@pytest.mark.parametrize("testdata", CLOSURE_FINDER_TESTS)
def test_closure_finder(testdata):
    closurefinder = ClosureFinder()
    closurefinder.input(testdata['input'])

    output = closurefinder.tree()
    assert len(output) == len(
        testdata['output']), "Test Muster unterscheiden sich hinsichtlich ihrer länge"

    for element in zip(output, testdata['output']):
        assert element[0] == element[1], testdata['description']
